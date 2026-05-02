"""
模板适配层 - 把通用结构映射到具体模板结构
关键：重命名标题，让内容更贴合意图
"""


def adapt_to_template(slides: list, template: str, intent: str) -> list:
    """
    把通用结构映射到模板结构
    """
    if template == "business":
        return adapt_business(slides, intent)

    # 默认返回原样
    return slides


def adapt_business(slides: list, intent: str) -> list:
    """
    商业模板适配
    根据意图重命名标题
    """
    mapped = []

    for slide in slides:
        title = slide.get("title", "")

        # 根据意图重命名
        if intent == "teach":
            title = map_teach_title(title)
        elif intent == "explain":
            title = map_explain_title(title)
        elif intent == "pitch":
            title = map_pitch_title(title)

        slide["title"] = title
        mapped.append(slide)

    return mapped


def map_teach_title(title: str) -> str:
    """教学方法标题映射"""
    mapping = {
        "问题": "为什么做不好",
        "方法1": "第1个关键",
        "方法2": "第2个关键",
        "方法3": "第3个关键",
        "总结": "总结",
        "封面": "封面"
    }
    return mapping.get(title, title)


def map_explain_title(title: str) -> str:
    """解释说明标题映射"""
    mapping = {
        "问题": "核心问题",
        "原因1": "原因一",
        "原因2": "原因二",
        "结论": "结论",
        "封面": "封面"
    }
    return mapping.get(title, title)


def map_pitch_title(title: str) -> str:
    """商业路演标题映射"""
    mapping = {
        "问题": "痛点",
        "方案": "解决方案",
        "市场": "市场规模",
        "优势": "核心优势",
        "总结": "总结",
        "封面": "封面"
    }
    return mapping.get(title, title)
