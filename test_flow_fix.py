# -*- coding: utf-8 -*-
"""测试积分兑换 Flow 修复（修正版）"""
import asyncio
import logging
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

# 设置英文日志格式避免乱码
logging.basicConfig(level=logging.WARNING, format='%(levelname)s | %(message)s')

from atguigu_ai.agent.agent import Agent

async def test():
    # 加载 Agent
    agent = Agent()
    result = agent.load("./ecs_demo")
    print(f"\nAgent loaded successfully")
    print(f"Policies: {[type(p).__name__ for p in agent.policy_ensemble.policies]}")

    sender_id = "test_user_001"
    tracker_store = agent.tracker_store
    message_processor = agent.message_processor

    # 重置状态
    await tracker_store.delete(sender_id)

    # 1. 测试查询积分
    print("\n" + "="*60)
    print("TEST 1: 查询我的积分")
    print("="*60)
    resp = await agent.handle_message("查询我的积分", sender_id)
    print(f"Response text: {resp}")
    for msg in getattr(resp, 'messages', []):
        print(f"  - {msg}")

    # 重置
    await tracker_store.delete(sender_id)

    # 2. 测试积分兑换
    print("\n" + "="*60)
    print("TEST 2: 我要兑换积分")
    print("="*60)
    resp = await agent.handle_message("我要兑换积分", sender_id)
    print(f"Response text: {resp}")
    for msg in getattr(resp, 'messages', []):
        print(f"  - {msg}")

    tracker = await tracker_store.retrieve(sender_id)
    if tracker:
        print(f"  active_flow: {tracker.active_flow}")
        print(f"  slots: {dict(tracker.slots) if hasattr(tracker, 'slots') else 'N/A'}")

    # 3. 选择商品 r001
    print("\n" + "="*60)
    print("TEST 3: /SetSlots(reward_id=r001)")
    print("="*60)
    resp = await agent.handle_message("/SetSlots(reward_id=r001)", sender_id)
    print(f"Response text: {resp}")
    for msg in getattr(resp, 'messages', []):
        print(f"  - {msg}")

    tracker = await tracker_store.retrieve(sender_id)
    if tracker:
        print(f"  active_flow: {tracker.active_flow}")
        print(f"  slots: {dict(tracker.slots) if hasattr(tracker, 'slots') else 'N/A'}")

    # 4. 确认兑换
    print("\n" + "="*60)
    print("TEST 4: /SetSlots(confirm_redeem=true)")
    print("="*60)
    resp = await agent.handle_message("/SetSlots(confirm_redeem=true)", sender_id)
    print(f"Response text: {resp}")
    for msg in getattr(resp, 'messages', []):
        print(f"  - {msg}")

    tracker = await tracker_store.retrieve(sender_id)
    if tracker:
        print(f"  active_flow: {tracker.active_flow}")
        print(f"  slots: {dict(tracker.slots) if hasattr(tracker, 'slots') else 'N/A'}")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test())
