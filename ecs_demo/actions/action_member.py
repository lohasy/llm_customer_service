# -*- coding: utf-8 -*-
"""
会员相关Action

实现会员积分查询、积分兑换等功能。
适配atguigu_ai框架Action接口。
"""

import logging
from typing import Any, Optional

from atguigu_ai.agent.actions import Action, ActionResult

logger = logging.getLogger(__name__)


class ActionQueryMemberPoints(Action):
    """查询会员积分和等级"""

    @property
    def name(self) -> str:
        return "action_query_member_points"

    async def run(
        self,
        tracker: Any,
        domain: Optional[Any] = None,
        **kwargs: Any,
    ) -> ActionResult:
        from actions.db import SessionLocal
        from actions.db_table_class import MemberPoints

        result = ActionResult()
        user_id = tracker.get_slot("user_id") or "1001"

        try:
            with SessionLocal() as session:
                member = (
                    session.query(MemberPoints)
                    .filter_by(user_id=user_id)
                    .first()
                )

                if not member:
                    result.add_response(
                        f"用户 {user_id} 暂无积分信息，快去购物获取积分吧！"
                    )
                    return result

                result.add_response(
                    f"您的当前积分为：{member.points} 分，"
                    f"会员等级：{member.member_level}"
                )

        except Exception as e:
            logger.error(f"查询会员积分失败: {e}")
            result.add_response("查询会员积分时出错，请稍后重试。")

        return result


class ActionShowRedeemableRewards(Action):
    """展示可兑换商品列表"""

    @property
    def name(self) -> str:
        return "action_show_redeemable_rewards"

    async def run(
        self,
        tracker: Any,
        domain: Optional[Any] = None,
        **kwargs: Any,
    ) -> ActionResult:
        from actions.db import SessionLocal
        from actions.db_table_class import MemberPoints, PointsRewards

        result = ActionResult()
        user_id = tracker.get_slot("user_id") or "1001"

        try:
            with SessionLocal() as session:
                # 查询用户积分
                member = (
                    session.query(MemberPoints)
                    .filter_by(user_id=user_id)
                    .first()
                )
                if not member:
                    result.add_response(
                        f"用户 {user_id} 暂无积分信息，快去购物获取积分吧！"
                    )
                    return result

                # 查询可兑换商品（用户积分 >= 所需积分 且 有库存）
                rewards = (
                    session.query(PointsRewards)
                    .filter(
                        PointsRewards.points_required <= member.points,
                        PointsRewards.stock > 0,
                    )
                    .all()
                )

                if not rewards:
                    result.add_response(
                        f"当前积分为 {member.points} 分，暂无符合条件可兑换的商品。"
                    )
                    return result

            # 生成按钮列表
            buttons = []
            for reward in rewards:
                buttons.append({
                    "title": (
                        f"{reward.reward_name} "
                        f"({reward.points_required}积分) "
                        f"库存:{reward.stock}"
                    ),
                    "payload": f"/SetSlots(reward_id={reward.reward_id})",
                })
            buttons.append({"title": "取消", "payload": "/SetSlots(reward_id=false)"})

            result.add_response(
                f"当前积分：{member.points} 分，请选择要兑换的商品：",
                buttons=buttons,
            )

        except Exception as e:
            logger.error(f"查询可兑换商品失败: {e}")
            result.add_response("查询商品列表时出错，请稍后重试。")

        return result


class ActionRedeemPoints(Action):
    """执行积分兑换"""

    @property
    def name(self) -> str:
        return "action_redeem_points"

    async def run(
        self,
        tracker: Any,
        domain: Optional[Any] = None,
        **kwargs: Any,
    ) -> ActionResult:
        from uuid import uuid4
        from datetime import datetime
        from actions.db import SessionLocal
        from actions.db_table_class import MemberPoints, PointsRewards, PointsRedemptionRecords

        result = ActionResult()
        user_id = tracker.get_slot("user_id") or "1001"
        reward_id = tracker.get_slot("reward_id")

        if not reward_id or reward_id == "false":
            result.add_response("未选择兑换商品。")
            return result

        try:
            with SessionLocal() as session:
                # 查询用户积分
                member = (
                    session.query(MemberPoints)
                    .filter_by(user_id=user_id)
                    .with_for_update()
                    .first()
                )
                if not member:
                    result.add_response("用户信息不存在。")
                    return result

                # 查询商品
                reward = (
                    session.query(PointsRewards)
                    .filter_by(reward_id=reward_id)
                    .with_for_update()
                    .first()
                )
                if not reward:
                    result.add_response("该商品不存在。")
                    return result

                # 检查积分是否足够
                if member.points < reward.points_required:
                    result.add_response(
                        f"积分不足！当前积分 {member.points} 分，"
                        f"需要 {reward.points_required} 分。"
                    )
                    return result

                # 检查库存
                if reward.stock <= 0:
                    result.add_response(f"{reward.reward_name} 库存不足。")
                    return result

                # 扣减积分
                member.points -= reward.points_required

                # 扣减库存
                reward.stock -= 1

                # 创建兑换记录
                record = PointsRedemptionRecords(
                    record_id="pr" + uuid4().hex[:16],
                    user_id=user_id,
                    reward_id=reward_id,
                    points_cost=reward.points_required,
                    redeem_time=datetime.now(),
                    status="completed",
                )
                session.add(record)
                session.commit()

                result.add_response(
                    f"兑换成功！消耗 {reward.points_required} 积分，"
                    f"获得 {reward.reward_name}。"
                )

        except Exception as e:
            logger.exception(f"积分兑换失败: {e}")
            result.add_response("兑换失败，请稍后重试。")

        return result
