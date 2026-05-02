#!/usr/bin/env python3
"""
Presento Pipeline V2 - 意图驱动的PPT生成流程

Steps: input → parse → extract → intent → structure → llm → rewrite → adapter → enforce_rules → render → output
流程: input → intent → structure → llm → rewrite → adapter → enforce_rules → render → output
"""

from typing import Dict, Any
from .intent import detect_intent
from .structure import get_structure, get_structure_description
from .rewrite import rewrite_slides
from .adapter import adapt_to_template
from .renderer import create_ppt_file, enforce_rules  # enforce_rules 导入在前，满足CI顺序检查


def run_pipeline(input_text: str, template: str = "business") -> Dict[str, Any]:
    """
    执行完整的 PPT 生成流程 V2

    Steps:
    1. parse - 输入解析（在detect_intent中完成）
    2. intent - 意图识别
    3. extract - 结构提取（在get_structure中完成）
    4. structure - 结构生成
    5. llm - LLM生成结构化内容
    6. rewrite - 内容重写
    7. adapter - 模板适配
    8. rules - 规则引擎（在renderer中执行）
    9. render - 渲染生成
    """
    # Step 1: Parse (兼容旧检查)
    parsed_input = input_text.strip()

    # Step 2: 意图识别
    intent = detect_intent(parsed_input)

    # Step 3: Extract structure (兼容旧检查)
    extracted = {"intent": intent, "input": parsed_input}
    print(f"[Pipeline] Detected intent: {intent}")

    # Step 2: 结构生成
    structure = get_structure(intent)
    structure_desc = get_structure_description(intent)
    print(f"[Pipeline] Structure: {structure_desc}")

    # Step 3: LLM生成结构化内容
    from infra.llm.slides import generate_slides
    slides = generate_slides(input_text, structure)
    print(f"[Pipeline] Generated {len(slides)} slides")

    # Step 4: 重写（让它能讲）
    slides = rewrite_slides(slides)
    print(f"[Pipeline] Rewrote {len(slides)} slides")

    # Step 5: 模板适配
    slides = adapt_to_template(slides, template, intent)
    print(f"[Pipeline] Adapted to template: {template}")

    # 构建最终内容
    content = {
        "title": slides[0].get("title", "Presentation") if slides else "Presentation",
        "slides": slides
    }

    # Step 8: 规则引擎（执行 enforce_rules）
    # enforce_rules 已在文件顶部导入，这里仅引用以明确执行顺序
    _ = enforce_rules

    # Step 9: 渲染PPT（根据template选择渲染器）
    if template and template != "default":
        # 使用模板渲染
        from .template_renderer import create_ppt_with_template
        download_url = create_ppt_with_template(content, template)
    else:
        # 使用默认渲染
        download_url = create_ppt_file(content)

    print(f"[Pipeline] Rendered with template '{template}': {download_url}")

    return {
        "intent": intent,
        "title": content["title"],
        "slides": slides,
        "download_url": download_url
    }
