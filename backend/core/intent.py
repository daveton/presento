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
    """
    text = text.lower()

    if any(k in text for k in ["产品", "市场", "用户", "商业", "融资", "方案"]):
        return "pitch"

    if any(k in text for k in ["如何", "步骤", "方法", "怎么做", "技巧", "教程"]):
        return "teach"

    if any(k in text for k in ["为什么", "原因", "原理", "是什么"]):
        return "explain"

    # 默认解释型
    return "explain"
