"""
重写引擎 V2 - 把"写的内容"变成"人会讲的话"
核心：拆句 → 重组 → 强化节奏
"""

import re


# 语义模式：用于拆句
PATTERNS = [
    ("不是.*而是", "contrast"),
    ("因为.*所以", "cause"),
    ("如果.*就", "condition"),
]


def clean_text(text: str) -> str:
    """清理标点符号"""
    return re.sub(r"[，。！？；]", "", text).strip()


def split_by_patterns(text: str) -> list:
    """
    按语义拆句
    不是..而是 / 因为..所以 / 如果..就
    """
    # 处理"不是..而是"
    if "不是" in text and "而是" in text:
        parts = text.split("而是")
        return [parts[0].replace("不是", "不是"), "是" + parts[1]]

    # 处理"因为..所以"
    if "因为" in text and "所以" in text:
        parts = text.split("所以")
        return [parts[0].replace("因为", ""), "所以" + parts[1]]

    # 处理"如果..就"
    if "如果" in text and "就" in text:
        parts = text.split("就")
        return [parts[0].replace("如果", ""), "就" + parts[1]]

    return [text]


def shorten(text: str, max_len=18) -> str:
    """截断到最大长度"""
    if len(text) <= max_len:
        return text
    return text[:max_len]


def rewrite_point_v2(text: str) -> list:
    """
    核心：把一句话变成"能讲的多行短句"
    原句 → 拆 → 重组 → 强化节奏
    """
    text = clean_text(text)

    # Step 1: 按语义模式拆句
    parts = split_by_patterns(text)

    results = []

    for p in parts:
        p = p.strip()
        if not p:
            continue

        # Step 2: 再细拆（按逗号）
        sub_parts = re.split(r"[，,]", p)

        for sp in sub_parts:
            sp = sp.strip()
            if not sp:
                continue

            # Step 3: 截断到合适长度
            sp = shorten(sp)
            results.append(sp)

    # 限制最多5条
    return results[:5]


def rewrite_title(title: str) -> str:
    """
    标题人话化（非常关键）
    """
    title = title.strip()

    # 模板替换
    replacements = {
        "问题": "为什么会这样",
        "原因": "背后的原因",
        "方法": "怎么做",
        "总结": "最后总结一下",
        "方案": "解决方案",
        "优势": "核心优势",
    }

    for k, v in replacements.items():
        if k in title:
            return v

    # 太长截断
    if len(title) > 18:
        return title[:18]

    return title


def rewrite_slides(slides: list) -> list:
    """
    对整页进行"讲话化重写"
    """
    new_slides = []

    for slide in slides:
        new_points = []

        for p in slide.get("points", []):
            rewritten = rewrite_point_v2(p)
            new_points.extend(rewritten)

        # 去重 & 限制数量
        seen = set()
        final_points = []

        for p in new_points:
            if p not in seen:
                final_points.append(p)
                seen.add(p)

        slide["points"] = final_points[:5]

        # 标题也要"人话化"
        slide["title"] = rewrite_title(slide.get("title", ""))

        new_slides.append(slide)

    return new_slides
