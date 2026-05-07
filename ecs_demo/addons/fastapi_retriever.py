# -*- coding: utf-8 -*-
"""FastAPI 知识库适配器

将外部 FastAPI 知识库服务适配为 InformationRetrieval 接口，
与 GraphRAG 并列，支持在 config.yml 中切换。

使用方式：
  config.yml:
    vector_store: addons.fastapi_retriever.FastAPIRetriever
"""

import logging
from typing import Any, Dict, List, Optional

import httpx

from atguigu_ai.retrieval.base_retriever import InformationRetrieval, SearchResult

logger = logging.getLogger(__name__)


class FastAPIRetriever(InformationRetrieval):
    """FastAPI 知识库检索器。

    通过 HTTP 调用外部 FastAPI 知识库服务的 /query 接口，
    将返回结果包装为 SearchResult。

    配置（endpoints.yml）：
        vector_store:
          base_url: http://localhost:8001
    """

    def __init__(self, embeddings: Any = None) -> None:
        super().__init__(embeddings)
        self._base_url: str = "http://localhost:8001"
        self._client: Optional[httpx.AsyncClient] = None

    def connect(self, config: Optional[Dict[str, Any]] = None) -> None:
        """连接知识库服务。

        从 config 中读取 base_url，初始化 HTTP 客户端。

        Args:
            config: 连接配置，含 base_url 字段
        """
        config = config or {}
        self._base_url = (
            config.get("base_url")
            or config.get("url")
            or "http://localhost:8001"
        )
        self._client = httpx.AsyncClient(
            base_url=self._base_url.rstrip("/"),
            timeout=httpx.Timeout(60.0),
        )
        logger.info("FastAPIRetriever 已连接: %s", self._base_url)

    async def search(
        self,
        query: str,
        top_k: int = 5,
        tracker_state: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """搜索知识库。

        调用 FastAPI 知识库服务的 POST /query 接口，
        返回 answer 字段作为搜索结果。

        Args:
            query: 用户查询文本
            top_k: 返回条数（当前知识库返回单条，忽略此参数）
            tracker_state: 对话状态（用于获取 session_id 等）

        Returns:
            SearchResult 列表
        """
        if not query or not query.strip():
            return []

        if self._client is None:
            logger.warning("HTTP 客户端未初始化，尝试使用默认地址连接")
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(60.0),
            )

        # 从 tracker_state 提取 session_id
        # tracker 中叫 sender_id，对应 FastAPI 的 session_id
        session_id = None
        if tracker_state:
            session_id = tracker_state.get("session_id") or tracker_state.get("sender_id")

        request_body: Dict[str, Any] = {
            "query": query.strip(),
            "is_stream": False,
        }
        if session_id:
            request_body["session_id"] = session_id

        try:
            response = await self._client.post("/query", json=request_body)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            logger.error("调用知识库失败: %s", e)
            return []
        except Exception as e:
            logger.error("解析知识库响应失败: %s", e)
            return []

        answer = data.get("answer", "")
        if not answer:
            logger.debug("知识库返回空 answer")
            return []

        logger.info("FastAPI 知识库返回: %s", answer[:200])

        return [
            SearchResult(
                text=answer,
                score=0.9,
                metadata={
                    "source": "fastapi_kb",
                    "session_id": data.get("session_id", ""),
                },
            )
        ]

    def close(self) -> None:
        """关闭 HTTP 连接。"""
        if self._client:
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self._client.aclose())
                else:
                    loop.run_until_complete(self._client.aclose())
            except RuntimeError:
                try:
                    import asyncio
                    asyncio.run(self._client.aclose())
                except Exception:
                    pass
        logger.info("FastAPIRetriever 连接已关闭")
