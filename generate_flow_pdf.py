# -*- coding: utf-8 -*-
"""
生成对话系统完整流程说明PDF
使用餐厅点餐类比，从小白视角解释整个项目流程
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def register_chinese_font():
    """注册中文字体"""
    # 尝试使用系统字体
    font_paths = [
        r"C:\Windows\Fonts\msyh.ttc",  # Windows 微软雅黑
        r"C:\Windows\Fonts\simsun.ttc",  # Windows 宋体
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                continue
    
    # 如果都失败，使用默认字体（中文可能显示异常）
    return 'Helvetica'


def create_styles(font_name):
    """创建样式"""
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        textColor=HexColor('#1a5276'),
        spaceAfter=20,
        alignment=TA_CENTER,
        leading=32
    ))
    
    # 一级标题
    styles.add(ParagraphStyle(
        name='Heading1Custom',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        textColor=HexColor('#2874a6'),
        spaceBefore=20,
        spaceAfter=10,
        leading=24
    ))
    
    # 二级标题
    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        textColor=HexColor('#3498db'),
        spaceBefore=15,
        spaceAfter=8,
        leading=20
    ))
    
    # 三级标题
    styles.add(ParagraphStyle(
        name='Heading3Custom',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        textColor=HexColor('#5dade2'),
        spaceBefore=12,
        spaceAfter=6,
        leading=16
    ))
    
    # 正文样式
    styles.add(ParagraphStyle(
        name='BodyTextCustom',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=11,
        textColor=HexColor('#2c3e50'),
        spaceAfter=8,
        leading=18,
        alignment=TA_LEFT
    ))
    
    # 代码块样式
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['BodyText'],
        fontName='Courier',
        fontSize=9,
        textColor=HexColor('#c0392b'),
        leftIndent=20,
        rightIndent=20,
        spaceBefore=8,
        spaceAfter=8,
        leading=14,
        backColor=HexColor('#f8f9fa')
    ))
    
    # 强调样式
    styles.add(ParagraphStyle(
        name='Emphasis',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=11,
        textColor=HexColor('#e74c3c'),
        spaceAfter=8,
        leading=18
    ))
    
    # 提示框样式
    styles.add(ParagraphStyle(
        name='TipBox',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        textColor=HexColor('#27ae60'),
        leftIndent=20,
        rightIndent=20,
        spaceBefore=10,
        spaceAfter=10,
        leading=16,
        backColor=HexColor('#e8f8f5')
    ))
    
    return styles


def create_role_table():
    """创建角色对应表"""
    data = [
        ['项目组件', '餐厅角色', '职责说明'],
        ['Channel', '前台接待', '接收用户消息，送到处理区'],
        ['Command Generator', '翻译官(LLM)', '理解用户话语，翻译成指令'],
        ['Command', '指令单', '具体的任务指令'],
        ['Command Processor', '调度员', '分发指令给不同部门'],
        ['Flow', '工作流程', '点餐/修改订单的标准流程'],
        ['FlowPolicy', '流程菜单管理员', '决定按流程该干什么'],
        ['Tracker', '小本本', '记录所有对话信息'],
        ['Action', '厨房', '真正干活的人（查数据库等）'],
    ]
    
    table = Table(data, colWidths=[4*cm, 4*cm, 7*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2874a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return table


def generate_pdf(output_path='对话系统完整流程说明.pdf'):
    """生成PDF文档"""
    font_name = register_chinese_font()
    styles = create_styles(font_name)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    story = []
    
    # 标题
    story.append(Paragraph('对话系统完整流程说明', styles['MainTitle']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('从小白视角理解整个项目的工作原理', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('—— 餐厅点餐类比版 ——', styles['Emphasis']))
    story.append(Spacer(1, 20))
    
    # 角色对应表
    story.append(Paragraph('🎭 核心角色对应表', styles['Heading1Custom']))
    story.append(Spacer(1, 10))
    story.append(create_role_table())
    story.append(Spacer(1, 20))
    
    # 完整流程
    story.append(Paragraph('📖 完整流程：从用户说话到系统响应', styles['Heading1Custom']))
    story.append(Spacer(1, 10))
    
    # 场景 1
    story.append(Paragraph('场景 1：用户说话 → 前台接待', styles['Heading2Custom']))
    story.append(Paragraph('用户说："我要修改订单的收货地址"', styles['BodyTextCustom']))
    story.append(Paragraph('Channel（前台接待）听到用户说话，把用户送到理解区（understand_node）。', 
                          styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 2
    story.append(Paragraph('场景 2：翻译官理解用户的话 → Command Generator', styles['Heading2Custom']))
    story.append(Paragraph('翻译官（LLM）的工作：把用户的话翻译成系统能懂的指令（Command）。', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('翻译官会看三样东西：', styles['BodyTextCustom']))
    story.append(Paragraph('1. Tracker（小本本）→ 之前的对话历史', styles['BodyTextCustom']))
    story.append(Paragraph('2. Flow列表（餐厅菜单）→ 有哪些流程可用', styles['BodyTextCustom']))
    story.append(Paragraph('3. 用户说的话 → "我要修改订单的收货地址"', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('翻译官思考后，写出指令单（生成Command）：', styles['BodyTextCustom']))
    story.append(Paragraph('• Command 1: StartFlowCommand("modify_order_receive_info")', styles['CodeBlock']))
    story.append(Paragraph('  意思："启动修改订单收货信息流程"', styles['BodyTextCustom']))
    story.append(Paragraph('• Command 2: SetSlotCommand("modify_type", "address")', styles['CodeBlock']))
    story.append(Paragraph('  意思："设置修改类型为地址"', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # Command 类型说明
    story.append(Paragraph('💡 Command 类型有哪些？', styles['Heading3Custom']))
    story.append(Paragraph('• StartFlowCommand → 启动流程', styles['BodyTextCustom']))
    story.append(Paragraph('• SetSlotCommand → 设置信息', styles['BodyTextCustom']))
    story.append(Paragraph('• AnswerCommand → 直接回答', styles['BodyTextCustom']))
    story.append(Paragraph('• SearchCommand → 搜索知识库', styles['BodyTextCustom']))
    story.append(Paragraph('• CannotHandleCommand → 听不懂', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 3
    story.append(Paragraph('场景 3：调度员分发指令 → Command Processor', styles['Heading2Custom']))
    story.append(Paragraph('调度员拿到指令单，逐条处理：', styles['BodyTextCustom']))
    story.append(Paragraph('第1条：StartFlowCommand → 在小本本上记录当前流程，压入流程栈', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('第2条：SetSlotCommand → 在小本本上记下：modify_type = "address"', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('处理完后，调度员决定：让流程菜单（FlowPolicy）来决定下一步。', 
                          styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 4
    story.append(Paragraph('场景 4：流程菜单决定下一步 → Flow Policy', styles['Heading2Custom']))
    story.append(Paragraph('FlowPolicy（流程菜单管理员）先检查：', styles['BodyTextCustom']))
    story.append(Paragraph('→ "刚才有干活吗？" tracker.latest_action_name = "action_listen"（在等待）', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('→ "没有，我可以决定下一步"', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('管理员看流程菜单（Flow配置），执行步骤1：设置goto槽位', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('→ 执行：tracker.set_slot("goto", "action_ask_order_id_before_delivered")', 
                          styles['CodeBlock']))
    story.append(Paragraph('→ 下一步是步骤2：收集订单号（但订单号现在是空的）', 
                          styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 5
    story.append(Paragraph('场景 5：继续执行 → Flow Executor', styles['Heading2Custom']))
    story.append(Paragraph('系统看到 FlowPolicy 的预测后：', styles['BodyTextCustom']))
    story.append(Paragraph('→ "有下一步（step_1），推进流程"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 更新小本本：当前步骤 = "step_1"', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('FlowPolicy 再次上场：', styles['BodyTextCustom']))
    story.append(Paragraph('→ "现在在步骤2（collect order_id）"', styles['BodyTextCustom']))
    story.append(Paragraph('→ "订单号是空的，需要问顾客"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 让厨房执行 action_ask_order_id', styles['BodyTextCustom']))
    story.append(Paragraph('→ 厨房根据 goto 值，查询可修改的订单', styles['BodyTextCustom']))
    story.append(Paragraph('→ 返回订单列表，带按钮供选择', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 6
    story.append(Paragraph('场景 6：防重复检查 → 关键机制', styles['Heading2Custom']))
    story.append(Paragraph('用户选择了订单后，FlowPolicy 上场前检查：', styles['BodyTextCustom']))
    story.append(Paragraph('检查1："刚才有干活吗？" → latest_action_name = "action_ask_order_id"', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('检查2："是等待动作吗？" → 不是等待，是真干活了', styles['BodyTextCustom']))
    story.append(Paragraph('检查3："流程在结束吗？" → 没有，流程还在进行中', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('结论："我刚让厨房干了活，得等顾客回复，不能连续发号施令"', 
                          styles['Emphasis']))
    story.append(Paragraph('返回：PolicyPrediction.abstain()（弃权）', styles['CodeBlock']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('💡 但这是新消息，系统会重置 latest_action_name = "action_listen"，现在可以重新决定了！', 
                          styles['TipBox']))
    story.append(Spacer(1, 10))
    
    # 场景 7
    story.append(Paragraph('场景 7：其他 Policy 的机会', styles['Heading2Custom']))
    story.append(Paragraph('如果 FlowPolicy 弃权了，谁来决定？', styles['BodyTextCustom']))
    story.append(Paragraph('策略竞争机制（Policy Ensemble）：', styles['BodyTextCustom']))
    story.append(Paragraph('1. FlowPolicy → "我弃权，刚干完活"', styles['BodyTextCustom']))
    story.append(Paragraph('2. EnterpriseSearchPolicy → "我也不需要，不是搜索问题"', styles['BodyTextCustom']))
    story.append(Paragraph('3. 默认策略 → "那就继续等待（action_listen）"', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('但如果用户问："你们餐厅几点关门？"', styles['BodyTextCustom']))
    story.append(Paragraph('→ FlowPolicy: "这不在流程里，我弃权"', styles['BodyTextCustom']))
    story.append(Paragraph('→ EnterpriseSearchPolicy: "我来回答！查知识库..."', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 8
    story.append(Paragraph('场景 8：条件分支 → 智能决策', styles['Heading2Custom']))
    story.append(Paragraph('FlowPolicy 看流程菜单中的条件：', styles['BodyTextCustom']))
    story.append(Paragraph('• 如果 order_id != "false" → 有订单，跳转到 get_order_detail', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('• 否则 → 没有订单，结束流程（END）', styles['BodyTextCustom']))
    story.append(Paragraph('→ 检查条件：order_id = 12345，满足条件！', styles['BodyTextCustom']))
    story.append(Paragraph('→ 推进到步骤3：让厨房查订单详情', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 9
    story.append(Paragraph('场景 9：流程循环 → 多次修改', styles['Heading2Custom']))
    story.append(Paragraph('用户选择：是的，还要改电话', styles['BodyTextCustom']))
    story.append(Paragraph('→ FlowPolicy 检查条件：满足循环条件', styles['BodyTextCustom']))
    story.append(Paragraph('→ 设置：receive_id = "modified"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 跳转回：select_modify_content', styles['BodyTextCustom']))
    story.append(Paragraph('→ 再次收集：这次改什么？用户说："电话"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 收集：receiver_phone', styles['BodyTextCustom']))
    story.append(Paragraph('→ 循环结束，去确认', styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    # 场景 10
    story.append(Paragraph('场景 10：流程结束 → 清理现场', styles['Heading2Custom']))
    story.append(Paragraph('最后一步：用户确认提交修改', styles['BodyTextCustom']))
    story.append(Paragraph('→ 执行最后一步动作：action_ask_set_receive_info', styles['BodyTextCustom']))
    story.append(Paragraph('→ 厨房执行：提交到数据库，修改成功！', styles['BodyTextCustom']))
    story.append(Paragraph('→ 设置 completing 标志：flow_frame.completing = True', styles['BodyTextCustom']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('下一轮：', styles['BodyTextCustom']))
    story.append(Paragraph('→ "检查：completing = True，虽然刚干了活，但流程要结束了"', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('→ "不弃权，处理结束逻辑"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 清理临时槽位，弹出流程栈，记录流程历史', styles['BodyTextCustom']))
    story.append(Paragraph('→ 说："修改完成！还有什么需要帮助的吗？"', styles['BodyTextCustom']))
    story.append(Paragraph('→ 回到：action_listen（等待新对话）', styles['BodyTextCustom']))
    
    story.append(PageBreak())
    
    # 流程时序图
    story.append(Paragraph('🔄 完整流程时序图', styles['Heading1Custom']))
    story.append(Spacer(1, 15))
    
    flow_data = [
        ['步骤', '组件', '动作'],
        ['1', '用户', '说话："我要修改订单收货地址"'],
        ['2', 'Channel', '前台接收消息，送到理解区'],
        ['3', 'Command Generator', '翻译官生成指令单（Command）'],
        ['4', 'Command Processor', '调度员分发指令，更新Tracker'],
        ['5', 'FlowPolicy', '流程菜单管理员决定下一步'],
        ['6', 'Flow Executor', '执行器推进流程步骤'],
        ['7', 'Action', '厨房执行具体操作（查数据库）'],
        ['8', 'Tracker', '更新小本本（记录信息）'],
        ['9', '系统', '等待用户下一次说话...'],
    ]
    
    flow_table = Table(flow_data, colWidths=[2*cm, 4*cm, 9*cm])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2874a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 20))
    
    # 核心要点
    story.append(Paragraph('🎯 核心要点总结', styles['Heading1Custom']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('1. Command = 指令单（启动流程、设置信息、回答问题）', styles['BodyTextCustom']))
    story.append(Paragraph('2. Flow = 工作流程（标准操作手册）', styles['BodyTextCustom']))
    story.append(Paragraph('3. Policy = 决策者（决定下一步干啥）', styles['BodyTextCustom']))
    story.append(Paragraph('4. Tracker = 小本本（记住所有信息）', styles['BodyTextCustom']))
    story.append(Paragraph('5. Action = 执行者（真正干活）', styles['BodyTextCustom']))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph('完整链路：', styles['Emphasis']))
    story.append(Paragraph('你说话 → 翻译官(Command) → 调度员 → Policy决策 → Flow流程 → Action执行 → 等待你说话', 
                          styles['CodeBlock']))
    story.append(Spacer(1, 20))
    
    # 防重入机制说明
    story.append(Paragraph('🛡️ 防重入机制详解', styles['Heading1Custom']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('为什么需要这个机制？', styles['Heading2Custom']))
    story.append(Paragraph('如果没有防重入：厨房查完订单 → 服务员立即又让厨房查 → 无限循环 → 厨房累死了！', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('有了防重入：厨房查完订单 → 服务员等顾客说话 → 正常流程！', 
                          styles['BodyTextCustom']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph('生活类比：', styles['Heading3Custom']))
    story.append(Paragraph('服务员就像一个懂规矩的员工：', styles['BodyTextCustom']))
    story.append(Paragraph('✅ 顾客点单 → 告诉厨房 → 等菜做好 → 端给顾客 → 等顾客吃完 → 再问要不要加菜', 
                          styles['BodyTextCustom']))
    story.append(Paragraph('❌ 不懂规矩：顾客点单 → 告诉厨房 → 又告诉厨房 → 又告诉厨房...（疯了）', 
                          styles['Emphasis']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('防重入机制就是："一次只干一件事，等顾客反馈再继续"', 
                          styles['TipBox']))
    
    # 构建PDF
    doc.build(story)
    print(f"✅ PDF生成成功：{output_path}")


if __name__ == '__main__':
    generate_pdf()
