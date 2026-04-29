# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

这是阿里云对话机器人框架 (`atguigu_ai`) 的 Python 实现，基于 LangGraph 实现对话编排。

## Architecture

```
用户消息 → Agent.handle_message()
    ↓
DialogueStateTracker (状态追踪)
    ↓
LLMCommandGenerator (LLM生成Command)
    ↓
CommandProcessor (执行命令)
    ↓
PolicyEnsemble (策略决策)
    ↓
Action执行 → NLG响应 → 返回用户
```

### Core Components

| 模块 | 路径 | 职责 |
|------|------|------|
| Agent | `atguigu_ai/agent/agent.py` | 主入口，协调组件 |
| DialogueStateTracker | `atguigu_ai/core/tracker.py` | 管理对话状态 |
| DialogueStack | `atguigu_ai/dialogue_understanding/stack/dialogue_stack.py` | 栈式上下文管理 |
| Domain | `atguigu_ai/core/domain.py` | 领域配置(槽位/动作/响应) |
| Commands | `atguigu_ai/dialogue_understanding/commands/` | LLM生成的命令 |
| Policies | `atguigu_ai/policies/` | 策略决策层 |
| Flows | `atguigu_ai/dialogue_understanding/flow/` | 对话流程定义 |

### Command 与 Action 职责

- **Command** (命令): LLM 生成，解析用户意图，更新 tracker 状态
- **Action** (动作): Policy 选择后执行，执行具体操作

两种设计模式：
1. **即时数据命令**: Command 直接操作 tracker (如 `StartFlowCommand.run()` 调用 `tracker.start_flow()`)
2. **动作触发命令**: Command 只返回事件，由 Action 执行 (如 `CancelFlowCommand`)

### DialogueStack 栈帧化设计

`dialogue_stack` 是唯一的状态管理源：
- `FlowStackFrame`: Flow 执行上下文
- `SearchStackFrame`: 知识库检索上下文
- `ChitChatStackFrame`: 闲聊上下文

通过 `DialogueStateTracker.active_flow` 派生属性访问当前活跃 Flow。

### Policy 策略链

`PolicyEnsemble` 按顺序执行：
1. `FlowPolicy` - 检测 Flow 栈帧
2. `EnterpriseSearchPolicy` - 检索知识库/闲聊/降级

## Commands

### 开发
```bash
# 运行 Demo
python -m atguigu_ai run --config ./ecs_demo

# Shell 交互
python -m atguigu_ai shell --config ./ecs_demo

# 训练
python -m atguigu_ai train ./data
```

### 测试
```bash
pytest tests/ -v
```

## Key Files

| 文件 | 说明 |
|------|------|
| `agent/agent.py:214` | `handle_message()` 主入口 |
| `core/tracker.py:132` | `DialogueStateTracker` 核心状态类 |
| `dialogue_understanding/stack/dialogue_stack.py:21` | `DialogueStack` 栈结构 |
| `dialogue_understanding/commands/base.py:102` | `Command` 抽象基类 |
| `policies/base_policy.py` | Policy 基类 |
| `dialogue_understanding/flow/flow.py` | Flow 定义 |

## Important Conventions

- Command 类用 `@register_command` 装饰器自动注册到全局注册表
- 所有 Command 必须实现 `command_name()`, `from_dict()`, `run()` 三个方法
- 使用 `@dataclass` 定义数据类
- Tracker 状态通过 `dialogue_stack` 统一管理，不直接存储 `active_flow`