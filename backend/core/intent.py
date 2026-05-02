"""
意图识别 - 规则版
识别用户输入内容的意图类型
"""


def detect_intent(text: str) -> str:
    """
    基于关键词识别意图类型
    teach: 教学/步骤
    explain: 解释/原因
    pitch: 商业/产品
    practice: 实践/案例分享
    report: 工作汇报
    """
    text = text.lower()

    # 工作汇报型（优先级高）
    if any(k in text for k in ["工作", "管理", "实践", "经验", "总结", "汇报", "成果", "项目", "推进", "完成"]):
        if any(k in text for k in ["能力", "关键", "核心", "管控", "协调"]):
            return "practice"  # 管理实践型
        return "report"  # 工作汇报型

    if any(k in text for k in ["产品", "市场", "用户", "商业", "融资", "方案"]):
        return "pitch"

    if any(k in text for k in ["如何", "步骤", "方法", "怎么做", "技巧", "教程"]):
        return "teach"

    if any(k in text for k in ["为什么", "原因", "原理", "是什么"]):
        return "explain"

    # 默认实践型（更通用）
    return "practice"
