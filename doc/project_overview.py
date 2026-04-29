# -*- coding: utf-8 -*-
"""生成项目介绍 PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
    chinese_font = 'SimSun'
except:
    try:
        pdfmetrics.registerFont(TTFont('MicrosoftYaHei', 'C:/Windows/Fonts/msyh.ttc'))
        chinese_font = 'MicrosoftYaHei'
    except:
        chinese_font = 'Helvetica'

# 创建 PDF
doc = SimpleDocTemplate(
    "D:/llm_customer_service/doc/project_overview_v2.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

# 自定义标题样式 - 使用中文字体
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontName=chinese_font,
    fontSize=24,
    spaceAfter=30,
    alignment=1,  # 居中
)

# 正文样式 - 使用中文字体
normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontName=chinese_font,
    fontSize=11,
    spaceAfter=10,
)

# 标题1样式
h1_style = ParagraphStyle(
    'Heading1',
    parent=styles['Heading1'],
    fontName=chinese_font,
    fontSize=16,
    spaceAfter=12,
    spaceBefore=20,
)

# 标题2样式
h2_style = ParagraphStyle(
    'Heading2',
    parent=styles['Heading2'],
    fontName=chinese_font,
    fontSize=13,
    spaceAfter=8,
    spaceBefore=12,
)

# 代码样式
code_style = ParagraphStyle(
    'Code',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=9,
    spaceAfter=10,
    leftIndent=20,
)

story = []

# 标题
story.append(Paragraph("LLM 对话机器人框架项目介绍", title_style))
story.append(Spacer(1, 0.5*cm))

# 章节 1
story.append(Paragraph("1. 项目概述", h1_style))
story.append(Paragraph("""
这是阿里云对话机器人框架 (atguigu_ai) 的 Python 实现，基于 LangGraph 实现对话编排。
是一个教学版的对话系统，适合理解对话系统的核心原理。
""", normal_style))
story.append(Spacer(1, 0.3*cm))

# 章节 2
story.append(Paragraph("2. 整体结构", h1_style))
story.append(Paragraph("""
<pre>
atguigu_ai/
├── agent/              # 核心 Agent
├── core/               # 核心模块 (Tracker, Domain, Slots)
├── dialogue_understanding/  # 对话理解 (Commands, Flows, Stack)
├── policies/           # 策略决策
├── nlg/               # 自然语言生成
├── retrieval/          # 向量检索 (RAG)
├── channels/           # 通信渠道 (REST, SocketIO, Console)
├── api/               # Web 服务
├── training/           # 训练模块
├── shared/             # 共享工具
└── cli/                # 命令行工具
</pre>
""", normal_style))
story.append(Spacer(1, 0.3*cm))

# 章节 3
story.append(Paragraph("3. 消息处理流程", h1_style))
story.append(Paragraph("""
<pre>
用户输入
   ↓
Agent.handle_message()
   ↓
LLMCommandGenerator (生成 Command)
   ↓
CommandProcessor (执行命令)
   ↓
PolicyEnsemble (策略决策)
   ↓
Action 执行 → NLG 响应 → 返回用户
</pre>
""", normal_style))
story.append(Spacer(1, 0.3*cm))

# 章节 4
story.append(Paragraph("4. 核心组件", h1_style))
story.append(Paragraph("""
<pre>
模块                 职责                    关键文件
-----------------------------------------------------------------
agent               主入口，协调各组件        agent.py:214
core/tracker        对话状态管理             tracker.py:132
core/domain         领域配置                 domain.py
commands            LLM 生成的命令           commands/base.py
stack               栈式上下文管理           dialogue_stack.py
flows               对话流程定义             flow.py
policies            策略决策                 base_policy.py
nlg                 响应文本生成             template_nlg.py
retrieval           向量检索 RAG            base_retriever.py
</pre>
""", normal_style))
story.append(Spacer(1, 0.3*cm))

# 章节 5
story.append(Paragraph("5. 核心概念", h1_style))

story.append(Paragraph("5.1 Command（命令）", h2_style))
story.append(Paragraph("""
LLM 根据用户输入生成，用于解析用户意图、更新 tracker 状态。
<ul>
<li>StartFlowCommand - 启动 Flow</li>
<li>SetSlotCommand - 设置槽位</li>
<li>ChitChatAnswerCommand - 闲聊回答</li>
</ul>
""", normal_style))

story.append(Paragraph("5.2 Tracker（状态追踪）", h2_style))
story.append(Paragraph("""
管理对话状态：槽位、Flow、对话历史。
dialogue_stack 是唯一状态源，active_flow 是派生属性。
""", normal_style))

story.append(Paragraph("5.3 DialogueStack（对话栈）", h2_style))
story.append(Paragraph("""
LIFO 栈结构，管理多轮对话上下文。
<ul>
<li>FlowStackFrame - Flow 执行上下文</li>
<li>SearchStackFrame - 知识库检索上下文</li>
<li>ChitChatStackFrame - 闲聊上下文</li>
</ul>
""", normal_style))

story.append(Paragraph("5.4 Policy（策略）", h2_style))
story.append(Paragraph("""
<ul>
<li>FlowPolicy - 检测 Flow 栈帧，执行 Flow 步骤</li>
<li>EnterpriseSearchPolicy - 知识库检索、闲聊、降级处理</li>
</ul>
""", normal_style))

story.append(Spacer(1, 0.3*cm))

# 章节 6
story.append(Paragraph("6. 完整流程详解", h1_style))

story.append(Paragraph("第1步：用户输入 → Agent 入口", h2_style))
story.append(Paragraph("""
Agent.handle_message(message, sender_id) → 获取/创建 DialogueStateTracker
""", normal_style))

story.append(Paragraph("第2步：LLM 生成 Command", h2_style))
story.append(Paragraph("""
DialogueStateTracker → LLMCommandGenerator.generate()
→ PromptBuilder → LLM API → CommandParser → Command 对象
""", normal_style))

story.append(Paragraph("第3步：CommandProcessor 执行命令", h2_style))
story.append(Paragraph("""
Command 对象列表 → CommandProcessor.process()
→ command.run(tracker) → 更新状态 → 返回 events + next_action
""", normal_style))

story.append(Paragraph("第4步：Policy 决策下一步", h2_style))
story.append(Paragraph("""
tracker → PolicyEnsemble.predict()
→ 按优先级遍历 Policies → 返回最佳 PolicyPrediction
""", normal_style))

story.append(Paragraph("第5步：Action 执行", h2_style))
story.append(Paragraph("""
PolicyPrediction → get_action(name) → Action.run()
→ 返回 ActionResult → NLG 生成响应文本
""", normal_style))

story.append(Paragraph("第6步：返回响应", h2_style))
story.append(Paragraph("""
ActionResult → 构建 MessageResponse → 保存 tracker → 返回给用户
""", normal_style))

story.append(Spacer(1, 0.3*cm))

# 章节 7
story.append(Paragraph("7. 关键文件速查", h1_style))
story.append(Paragraph("""
<pre>
步骤            文件                             关键方法
-----------------------------------------------------------------
入口            agent/agent.py                 handle_message()
生成命令        generator/llm_generator.py      generate()
执行命令        processor/command_processor.py process()
策略决策        policy_ensemble.py            predict()
执行动作        actions.py                     get_action()
</pre>
""", normal_style))

story.append(Spacer(1, 0.3*cm))

# 章节 8
story.append(Paragraph("8. 运行命令", h1_style))
story.append(Paragraph("""
<pre>
# 运行 Demo
python -m atguigu_ai run --config ./ecs_demo

# Shell 交互
python -m atguigu_ai shell --config ./ecs_demo

# 训练
python -m atguigu_ai train ./data
</pre>
""", normal_style))

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Generated by Claude Code", normal_style))

# 构建 PDF
doc.build(story)
print("PDF 生成成功: doc/project_overview.pdf")
