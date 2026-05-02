"""
结构生成 - 基于意图生成PPT骨架
"""

# 预定义结构模板
STRUCTURES = {
    "teach": [
        "封面",
        "问题",
        "方法1",
        "方法2",
        "方法3",
        "总结"
    ],
    "explain": [
        "封面",
        "问题",
        "原因1",
        "原因2",
        "结论"
    ],
    "pitch": [
        "封面",
        "问题",
        "方案",
        "市场",
        "优势",
        "总结"
    ]
}


def get_structure(intent: str) -> list:
    """
    根据意图获取对应的PPT结构
    """
    return STRUCTURES.get(intent, STRUCTURES["explain"])


def get_structure_description(intent: str) -> str:
    """
    获取结构的文字描述（用于Prompt）
    """
    structure = get_structure(intent)
    return " → ".join(structure)
