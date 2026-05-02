"""
Slide生成模块 - 基于结构生成PPT内容
Pipeline V2 专用
"""

import os
import json


def generate_slides(text: str, structure: list) -> list:
    """
    Pipeline V2: 基于结构生成幻灯片内容
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("[LLM] No API key, using structure-based mock")
        return _generate_slides_from_structure(structure, text)

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)

        structure_desc = " → ".join(structure)
        prompt = f"""你是一个专业的PPT内容设计师。

请根据以下内容，生成PPT：

结构：
{structure_desc}

要求：
- 严格按照结构生成每一页
- 每页2-5个要点
- 每条≤20字
- 要自然、可讲
- 标题要吸引人

格式（JSON）：
[
  {{
    "title": "页面标题",
    "points": ["要点1", "要点2", "要点3"]
  }}
]

内容：
{text[:2000]}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional presentation designer. Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=2000
        )

        result = json.loads(response.choices[0].message.content)

        if isinstance(result, dict) and "slides" in result:
            slides = result["slides"]
        elif isinstance(result, list):
            slides = result
        else:
            slides = [result]

        print(f"[LLM] Generated {len(slides)} slides")
        return slides

    except Exception as e:
        print(f"[LLM] Error: {e}, using mock")
        return _generate_slides_from_structure(structure, text)


def _generate_slides_from_structure(structure: list, text: str) -> list:
    """基于结构生成Mock内容"""
    slides = []
    content_preview = text[:30] if len(text) < 50 else "内容分析"

    for item in structure:
        if item == "封面":
            slides.append({"title": content_preview, "points": ["核心主题提炼"]})
        elif item == "问题":
            slides.append({"title": "核心问题", "points": ["用户痛点分析", "问题根源", "影响范围"]})
        elif item == "方法1":
            slides.append({"title": "第1个关键", "points": ["第一步：明确目标", "第二步：执行策略", "第三步：验证效果"]})
        elif item == "方法2":
            slides.append({"title": "第2个关键", "points": ["调整方向", "优化细节", "持续迭代"]})
        elif item == "方法3":
            slides.append({"title": "第3个关键", "points": ["总结规律", "复制经验", "扩大影响"]})
        elif item == "原因1":
            slides.append({"title": "原因一", "points": ["直接原因", "深层因素", "数据支持"]})
        elif item == "原因2":
            slides.append({"title": "原因二", "points": ["外部因素", "内部因素", "关键变量"]})
        elif item == "结论":
            slides.append({"title": "结论", "points": ["核心发现", "行动建议", "下一步计划"]})
        elif item == "方案":
            slides.append({"title": "解决方案", "points": ["产品定位", "核心功能", "差异化优势"]})
        elif item == "市场":
            slides.append({"title": "市场规模", "points": ["目标用户", "市场容量", "增长趋势"]})
        elif item == "优势":
            slides.append({"title": "核心优势", "points": ["技术优势", "团队优势", "资源优势"]})
        elif item == "总结":
            slides.append({"title": "总结", "points": ["核心要点回顾", "关键行动", "预期成果"]})
        else:
            slides.append({"title": item, "points": ["要点说明", "详细内容", "关键结论"]})

    return slides
