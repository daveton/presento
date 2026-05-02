"""
重写引擎 - 让内容更像人讲话
够用版本，先跑起来再优化
"""

import re


def clean_text(text: str) -> str:
    """清理标点符号"""
    text = re.sub(r"[，。！？；]", "", text)
    return text.strip()


def split_short(sentence: str) -> list:
    """按逻辑切分短句"""
    if "，" in sentence:
        return sentence.split("，")
    return [sentence]


def rewrite_point(text: str) -> list:
    """
    重写单个要点
    - 清理标点
    - 切分短句
    - 长度限制
    """
    text = clean_text(text)
    parts = split_short(text)

    result = []
    for p in parts:
        p = p.strip()

        # 长度限制
        if len(p) > 20:
            p = p[:20]

        if p:
            result.append(p)

    return result


def rewrite_slides(slides: list) -> list:
    """
    重写所有幻灯片
    - 每个要点重写
    - 限制最多5条
    """
    new_slides = []

    for slide in slides:
        points = slide.get("points", [])

        new_points = []
        for p in points:
            new_points.extend(rewrite_point(p))

        # 限制5条
        slide["points"] = new_points[:5]

        new_slides.append(slide)

    return new_slides


def enhance_for_speaking(text: str) -> str:
    """
    增强可讲性（简单版）
    后续可扩展更多替换规则
    """
    # 书面语 → 口语化
    replacements = [
        ("因为", "原因："),
        ("所以", "结果是"),
        ("通过", "用"),
        ("进行", ""),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text
