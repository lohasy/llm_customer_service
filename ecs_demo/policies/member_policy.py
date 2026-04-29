# -*- coding: utf-8 -*-
"""
会员策略 (MemberPolicy)

负责检测用户消息中的会员相关意图，自动启动会员 Flow。
优先级介于 FlowPolicy(100) 和 EnterpriseSearchPolicy(50) 之间。

工作流程：
1. 检查是否有活跃 Flow（有则 abstain，让 FlowPolicy 处理）
2. 获取当前用户消息，做关键字匹配
3. 匹配成功 → 调用 tracker.start_flow() 启动对应 Flow → 返回 action_listen
4. 匹配失败 → abstain，交给 EnterpriseSearchPolicy 处理
"""

import logging
import re
from typing import Any, Optional, TYPE_CHECKING

from atguigu_ai.policies.base_policy import Policy, PolicyPrediction
from atguigu_ai.policies.policy_ensemble import EnsembleConfig
from atguigu_ai.shared.constants import ACTION_LISTEN

if TYPE_CHECKING:
    from atguigu_ai.core.tracker import DialogueStateTracker
    from atguigu_ai.core.domain import Domain
    from atguigu_ai.dialogue_understanding.flow import FlowsList

logger = logging.getLogger(__name__)

# 意图匹配规则: (正则, 对应 Flow 名称)
INTENT_RULES = [
    # 查询积分：积分+查询/多少/查看/等级/升级
    (r"(查询|查看|看下|我的).*(积分)|(积分).*(查询|查看|有多少|多少|等级|升级|级别)", "query_member_points"),
    # 会员等级/升级
    (r"(会员|等级|升级).*(等级|会员|升级|权益)", "query_member_points"),
    # 积分兑换
    (r"(积分).*(兑换|换|商品|礼品|礼物)|(兑换|换).*(积分|商品|礼品)", "points_redemption"),
]


class MemberPolicy(Policy):
    """会员策略：检测会员意图，启动会员 Flow。"""

    DEFAULT_PRIORITY = 80

    def __init__(
        self,
        **kwargs: Any,
    ):
        from atguigu_ai.policies.base_policy import PolicyConfig
        super().__init__(PolicyConfig(priority=80), **kwargs)

    def should_predict(
        self,
        tracker: "DialogueStateTracker",
    ) -> bool:
        """只在没有活跃 Flow 时预测，避免打断已有流程。"""
        return tracker.active_flow is None

    async def predict(
        self,
        tracker: "DialogueStateTracker",
        domain: Optional["Domain"] = None,
        flows: Optional["FlowsList"] = None,
        **kwargs: Any,
    ) -> PolicyPrediction:
        """检测用户消息，匹配会员意图并启动 Flow。"""
        # 获取最新用户消息
        latest_message = tracker.latest_message
        if not latest_message:
            logger.debug("[MemberPolicy] 无用户消息，abstain")
            return PolicyPrediction.abstain(self.name)

        text = latest_message.text if hasattr(latest_message, 'text') else str(latest_message)
        if not text:
            return PolicyPrediction.abstain(self.name)

        # 匹配意图
        matched_flow = self._match_intent(text)

        if not matched_flow:
            logger.debug(f"[MemberPolicy] 未匹配会员意图: {text}")
            return PolicyPrediction.abstain(self.name)

        # 检查 Flow 是否存在
        if flows:
            flow = flows.get_flow(matched_flow)
            if not flow:
                logger.warning(f"[MemberPolicy] Flow '{matched_flow}' 不存在")
                return PolicyPrediction.abstain(self.name)

        # 启动 Flow
        logger.info(f"[MemberPolicy] 匹配意图 '{matched_flow}'，启动 Flow")
        tracker.start_flow(matched_flow)

        return PolicyPrediction(
            action=ACTION_LISTEN,
            confidence=1.0,
            policy_name=self.name,
            metadata={"started_flow": matched_flow},
        )

    def _match_intent(self, text: str) -> Optional[str]:
        """对用户文本做关键字匹配，返回匹配的 Flow 名称。"""
        for pattern, flow_name in INTENT_RULES:
            if re.search(pattern, text):
                logger.debug(f"[MemberPolicy] 匹配成功: pattern='{pattern}' → flow='{flow_name}'")
                return flow_name
        return None
