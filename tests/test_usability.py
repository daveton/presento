#!/usr/bin/env python3
"""
可用性测试（产品价值验证）
不是测代码对不对，而是测PPT能不能直接讲
"""

from test_cases import TEST_CASES

# ==============================
# 可讲性评分（核心）
# ==============================

def speakability_score(slide: dict) -> int:
    """
    可讲性评分 - PPT不是用来读的，是用来讲的
    满分100，合格线70
    """
    score = 100
    points = slide.get("points", [])
    
    for p in points:
        # 太长 → 讲不顺
        if len(p) > 15:
            score -= 10
        elif len(p) > 12:
            score -= 5
        
        # 书面语 → 难出口
        if "的" in p:
            score -= 2
        if "是" in p:
            score -= 2
        if "通过" in p:
            score -= 3
        if "进行" in p:
            score -= 3
        
        # 动词开头 → 更顺口
        good_starts = ["用", "做", "抓", "搞", "打", "上", "下"]
        if any(p.startswith(s) for s in good_starts):
            score += 3
        
        # 有节奏感（短句+箭头）
        if "→" in p or ">" in p:
            score += 5
        
        # 有数字 → 更具体
        if any(c.isdigit() for c in p):
            score += 3
    
    return max(0, score)


# ==============================
# 惊喜感评分
# ==============================

def surprise_score(slide: dict) -> int:
    """
    惊喜感评分 - 有没有"哦？"时刻
    """
    score = 0
    points = slide.get("points", [])
    title = slide.get("title", "")
    
    # 反常识表达
    reverse_patterns = ["不是", "不要", "错了", "误区", "陷阱"]
    for p in points:
        if any(pat in p for pat in reverse_patterns):
            score += 10
    
    # 数字冲击
    for p in points:
        if "%" in p or "倍" in p or "万" in p:
            score += 5
    
    # 对比结构
    for p in points:
        if "vs" in p.lower() or "对比" in p or "区别" in p:
            score += 5
    
    # 标题有张力
    if any(c in title for c in ["！", "？", "死", "杀", "爆", "秘密"]):
        score += 10
    
    return min(100, score)


# ==============================
# 信息密度评分
# ==============================

def density_score(slide: dict) -> int:
    """
    信息密度评分 - 会不会太挤
    """
    score = 100
    points = slide.get("points", [])
    
    # 太多要点 → 太挤
    if len(points) > 5:
        score -= 20
    elif len(points) > 4:
        score -= 10
    
    # 每页总字数
    total_chars = sum(len(p) for p in points)
    if total_chars > 60:
        score -= 15
    elif total_chars > 50:
        score -= 10
    
    return max(0, score)


# ==============================
# 综合可用性评分
# ==============================

def usability_score(slide: dict) -> dict:
    """
    综合可用性评分
    """
    speak = speakability_score(slide)
    surprise = surprise_score(slide)
    density = density_score(slide)
    
    # 加权综合
    total = speak * 0.5 + surprise * 0.3 + density * 0.2
    
    return {
        "speakability": speak,
        "surprise": surprise,
        "density": density,
        "total": round(total),
        "usable": total >= 70
    }


# ==============================
# 用户反馈模板
# ==============================

USER_FEEDBACK_TEMPLATE = """
=== PPT 可用性测试反馈 ===

测试内容：{content_name}
测试日期：{date}

【基础检查】
□ 没有明显错误（错别字、重复内容）
□ 结构清晰（有标题、有要点）
□ 页数合适（≤10页）

【核心问题】（只问这3个）
1. 你会用这个PPT去讲吗？
   □ 会  □ 不会  □ 需要大改

2. 哪一页最顺/最不顺？
   最顺：_______
   最不顺：_______

3. 看完有"哦？"的感觉吗？
   □ 有  □ 没有

【具体反馈】
- 讲不顺的地方：
- 想改的内容：
- 总体评价（1-10分）：_______

【建议】
如果要改，改哪里？
"""


def run_usability_test():
    """运行可用性测试框架"""
    print("🔥 Presento 可用性测试框架")
    print("=" * 50)
    print()
    print("测试维度：")
    print("  1. 可讲性 (speakability) - 能不能顺口讲")
    print("  2. 惊喜感 (surprise) - 有没有'哦？'")
    print("  3. 信息密度 (density) - 会不会太挤")
    print()
    print("合格标准：综合评分 ≥ 70 且 可讲性 ≥ 60")
    print()
    print("=" * 50)
    print()
    print("下一步：")
    print("1. 生成真实PPT")
    print("2. 自己对着讲一遍")
    print("3. 找人试用，收集反馈")
    print()
    print("反馈模板已准备（USER_FEEDBACK_TEMPLATE）")


if __name__ == "__main__":
    run_usability_test()
