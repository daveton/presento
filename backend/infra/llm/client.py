import os
import json
from typing import Dict, Any, List, Tuple

# 设置 OpenAI API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ============================================================
# 🥇 Step 1: 结构提取 Prompt
# ============================================================
STEP1_SYSTEM_PROMPT = """You are an expert content analyst.

Your job is to extract the core ideas from the user's content and organize them into a clear logical structure for a presentation.

Rules:
1. Identify the main topic
2. Break content into 3-8 key sections
3. Each section should represent ONE idea
4. Keep descriptions concise
5. Output JSON only, no explanation

Output format:
{
  "title": "main topic",
  "sections": [
    {
      "title": "section title",
      "summary": "short explanation"
    }
  ]
}"""

STEP1_USER_PROMPT = """{input_text}"""


# ============================================================
# 🥈 Step 2: PPT重写 Prompt（核心 - 80分关键）
# ============================================================
STEP2_SYSTEM_PROMPT = """You are a professional presentation designer.

Your job is to convert structured content into a clean, ready-to-use presentation.

You are NOT summarizing.
You are rewriting for presentation.

Rewrite aggressively:
- Shorter
- Clearer
- More punchy

CRITICAL RULES (must follow strictly):

1. Language:
- Use simplified Chinese
- Make it sound natural for speaking, not writing

2. Title rules:
- Each slide title ≤ 22 Chinese characters
- Must be clear and punchy

3. Bullet rules:
- Each slide must have 2-5 bullet points
- Each bullet ≤ 20 Chinese characters
- Use short phrases, NOT full sentences
- Avoid filler words

4. Style:
- Make content easy to present
- Prefer rhythm and contrast
- Break long ideas into multiple bullets

5. Structure:
- First slide must be a cover
- Total slides ≤ 10

6. Output format:
- JSON ONLY
- No explanation
- No markdown

IMPORTANT - Good vs Bad Examples:

✓ GOOD (short, punchy, presentable):
"前3秒决定生死"
"抓不住 → 被划走"

✗ BAD (summary style, not for PPT):
"短视频需要在前三秒吸引用户注意力"
"如果抓不住用户注意力就会被划走"

Output format:
{
  "title": "PPT标题",
  "slides": [
    {
      "type": "cover",
      "title": "封面标题",
      "subtitle": "副标题"
    },
    {
      "type": "content",
      "title": "页面标题",
      "points": ["要点1", "要点2"]
    }
  ]
}"""

STEP2_USER_PROMPT = """Convert the following structure into a presentation:

{step1_output_json}"""


# ============================================================
# 🥉 Step 3: 加强版 Prompt（用于重试，质量不足时）
# ============================================================
STRICT_STEP2_PROMPT = """You are a professional presentation designer.

🚨 FINAL WARNING - ANY VIOLATION WILL CAUSE ERRORS:

1. Each bullet point MUST be ≤ 20 Chinese characters
2. Each title MUST be ≤ 22 Chinese characters
3. Use SHORT PHRASES ONLY - cut words mercilessly

Examples of acceptable output:
"效率翻倍" (4 chars)
"成本过高" (4 chars)
"3秒定生死" (5 chars)
"抓不住 → 被划走" (9 chars with arrow)

Output MUST be valid JSON."""


def is_valid_input(text: str) -> Tuple[bool, str]:
    """
    输入验证
    """
    if not text or len(text.strip()) < 50:
        return False, "Content too short. Please provide at least 50 characters."
    
    if len(text) > 5000:
        return False, "Content too long. Maximum 5000 characters allowed."
    
    if text.count('http') > 10:
        return False, "Too many URLs detected. Please paste the actual content text."
    
    return True, "OK"


def score_ppt(content: Dict[str, Any]) -> int:
    """
    质量评分系统
    满分100，合格线70
    """
    score = 100
    slides = content.get("slides", [])
    
    for slide in slides:
        # 要点数量检查
        points = slide.get("points", [])
        if len(points) < 2:
            score -= 20
        elif len(points) > 5:
            score -= 15
        
        # 要点长度检查
        for p in points:
            if len(p) > 20:
                score -= 10
                break
        
        # 标题长度检查
        title = slide.get("title", "")
        if len(title) > 22:
            score -= 15
        
        # 空内容检查
        if slide.get("type") == "content" and not points:
            score -= 25
    
    return max(0, score)


def enforce_rules(content: Dict[str, Any]) -> Dict[str, Any]:
    """
    强制应用规则 - 不警告，直接裁剪
    """
    # 强制主标题
    content["title"] = content.get("title", "Presentation")[:22]
    
    for slide in content.get("slides", []):
        # 强制标题
        slide["title"] = slide.get("title", "")[:22]
        
        # 强制要点数量和长度
        if "points" in slide:
            points = slide["points"][:5]  # 最多5条
            points = [p[:20] for p in points]  # 每条最多20字
            slide["points"] = points
    
    return content


def add_constraints_hint(input_text: str, attempt: int) -> str:
    """
    为重试添加更强的约束提示
    """
    hints = [
        "\n\nRemember: Keep titles under 22 characters and bullet points under 20 characters.",
        "\n\nCRITICAL: Short phrases only. Use abbreviations if needed. Max 20 chars per bullet.",
        "\n\nFINAL WARNING: Any text over 20 chars will be cut. Write short, punchy phrases."
    ]
    return input_text + hints[min(attempt, len(hints) - 1)]


async def generate_ppt_content(input_text: str) -> Dict[str, Any]:
    """
    完整的两阶段PPT生成流程（目标：80分产品质量）
    
    Step 1: 结构提取 - 理解内容逻辑
    Step 2: PPT重写 - 转化为演讲友好的短句
    Step 3: 质量评分 - 确保符合规则
    Step 4: 强制规则 - 兜底裁剪
    """
    # 检查API密钥
    if not OPENAI_API_KEY:
        print("No API key found, using mock content")
        return _generate_mock_content(input_text)
    
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        # ============================================================
        # 🥇 Step 1: 结构提取
        # ============================================================
        print("Step 1: Extracting content structure...")
        step1_response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": STEP1_SYSTEM_PROMPT},
                {"role": "user", "content": STEP1_USER_PROMPT.format(input_text=input_text[:4000])}
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1000
        )
        
        step1_result = step1_response.choices[0].message.content
        print(f"Step 1 complete: {len(step1_result)} chars extracted")
        
        # ============================================================
        # 🥈 Step 2: PPT重写（带重试机制）
        # ============================================================
        step2_input = step1_result
        
        for attempt in range(3):
            print(f"Step 2.{attempt + 1}: Rewriting for presentation...")
            
            # 选择提示词
            if attempt == 0:
                system_prompt = STEP2_SYSTEM_PROMPT
            else:
                system_prompt = STRICT_STEP2_PROMPT
            
            response = await client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": STEP2_USER_PROMPT.format(step1_output_json=step2_input)}
                ],
                response_format={"type": "json_object"},
                temperature=0.6 if attempt == 0 else 0.4,
                max_tokens=2000
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                
                # 质量评分
                score = score_ppt(result)
                print(f"Quality score: {score}/100")
                
                if score >= 70:
                    print("✓ Quality check passed!")
                    return enforce_rules(result)
                
                print(f"✗ Quality too low ({score}), retrying with stronger prompt...")
                step2_input = result  # 用当前结果继续优化
                
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}, retrying...")
                continue
        
        # ============================================================
        # 🥉 Step 3: 强制规则兜底
        # ============================================================
        print("⚠️ All retries failed, applying forced rules...")
        return enforce_rules(result)
        
    except Exception as e:
        print(f"Error: {e}, falling back to mock")
        return _generate_mock_content(input_text)


def _generate_mock_content(input_text: str) -> Dict[str, Any]:
    """
    生成 mock 内容用于测试
    实际使用时替换为真实 LLM 调用
    """
    # 简单的内容分析，根据输入长度生成不同页数
    preview = input_text[:100]
    
    return {
        "title": "Video Content Analysis",
        "slides": [
            {
                "type": "cover",
                "title": "Video Content Analysis",
                "subtitle": f"Based on: {preview}..."
            },
            {
                "type": "content",
                "title": "Core Insights",
                "points": [
                    "Key message extracted",
                    "Main argument identified", 
                    "Supporting points found"
                ]
            },
            {
                "type": "content",
                "title": "Actionable Takeaways",
                "points": [
                    "Apply strategy immediately",
                    "Share with your team",
                    "Implement best practices"
                ]
            },
            {
                "type": "summary",
                "title": "Next Steps",
                "points": [
                    "Review the full analysis",
                    "Create action plan",
                    "Track progress weekly"
                ]
            }
        ]
    }
