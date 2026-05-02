"""
模板配置 - Lite 版
预定义固定模板，不解析，只使用
"""

import os

# 模板根目录
TEMPLATE_DIR = "resources/templates"

# 预定义模板配置
TEMPLATES = {
    "minimal": {
        "name": "极简黑白",
        "description": "通用简洁风格",
        "file": os.path.join(TEMPLATE_DIR, "minimal.pptx"),
        "layouts": {
            "cover": 0,      # 封面
            "content": 1,    # 标题+内容
        }
    },
    "business": {
        "name": "商业风格",
        "description": "演示文稿4风格",
        "file": os.path.join(TEMPLATE_DIR, "演示文稿4.pptx"),
        "layouts": {
            "cover": 0,      # 封面
            "content": 1,    # 标题+内容
            "split": 2,      # 两列布局
        }
    },
    "teach": {
        "name": "内容讲解",
        "description": "适合知识讲解",
        "file": os.path.join(TEMPLATE_DIR, "teach.pptx"),
        "layouts": {
            "cover": 0,
            "content": 1,
            "highlight": 2,  # 重点突出
        }
    }
}


def get_template_config(template_id: str) -> dict:
    """获取模板配置"""
    return TEMPLATES.get(template_id, TEMPLATES["business"])


def list_templates() -> list:
    """列出所有可用模板"""
    return [
        {
            "id": k,
            "name": v["name"],
            "description": v["description"]
        }
        for k, v in TEMPLATES.items()
    ]


def choose_layout(slide: dict, template_id: str = "business") -> str:
    """
    根据内容选择合适的layout
    """
    config = get_template_config(template_id)
    layouts = config.get("layouts", {})

    # 封面
    if slide.get("type") == "cover":
        return "cover"

    # 根据要点数量选择
    points = slide.get("points", [])
    if len(points) <= 3 and "content" in layouts:
        return "content"

    # 默认使用第一个可用layout
    return list(layouts.keys())[0] if layouts else "content"
