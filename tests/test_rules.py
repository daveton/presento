#!/usr/bin/env python3
"""
规则引擎独立测试（不依赖外部库）
"""

# 直接复制核心常量用于测试
MAX_TITLE_LEN = 22
MAX_POINTS = 5
MAX_POINT_LEN = 20

def trim_text(text, max_len):
    return text[:max_len]

def clean_text(text):
    return text.replace("，", "").replace("。", "")

def split_points(points):
    """自动分页"""
    result = []
    for i in range(0, len(points), MAX_POINTS):
        result.append(points[i:i + MAX_POINTS])
    return result

def rewrite_point(text):
    """内容优化"""
    text = clean_text(text)
    if len(text) > MAX_POINT_LEN:
        text = text[:MAX_POINT_LEN]
    if "因为" in text:
        text = text.replace("因为", "原因：")
    return text

def enforce_rules(slides):
    """强制规则引擎"""
    new_slides = []
    
    for slide in slides:
        slide_type = slide.get("type", "content")
        
        if slide_type == "cover":
            new_slides.append({
                "type": "cover",
                "title": trim_text(slide.get("title", ""), MAX_TITLE_LEN),
                "subtitle": trim_text(slide.get("subtitle", ""), 40)
            })
            continue
        
        title = trim_text(slide.get("title", ""), MAX_TITLE_LEN)
        points = slide.get("points", [])
        
        points = [rewrite_point(p) for p in points]
        points = [p[:MAX_POINT_LEN] for p in points]
        
        split = split_points(points)
        
        for part in split:
            new_slides.append({
                "type": "content",
                "title": title,
                "points": part
            })
    
    return new_slides[:10]

def score_slides(slides):
    """质量评分"""
    score = 100
    
    for slide in slides:
        if slide["type"] == "content":
            pts = slide.get("points", [])
            
            if len(pts) < 2:
                score -= 20
            
            for p in pts:
                if len(p) > MAX_POINT_LEN:
                    score -= 5
    
    return score

def test_rule_enforcement():
    """测试规则引擎"""
    print("\n=== Testing Rule Enforcement ===")
    
    slides = [
        {
            "type": "cover",
            "title": "这是一个非常长的标题超过了22个字符的限制",
            "subtitle": "副标题"
        },
        {
            "type": "content",
            "title": "章节标题也很长很长很长",
            "points": [
                "这是一个超过20个字符的要点内容",
                "短句",
                "这也超过20字符了哈哈哈",
                "点4",
                "点5",
                "点6",
                "点7"
            ]
        }
    ]
    
    result = enforce_rules(slides)
    
    # 验证封面标题
    assert len(result[0]["title"]) <= MAX_TITLE_LEN, f"封面标题过长: {len(result[0]['title'])}"
    print(f"✓ 封面标题截断: {result[0]['title']}")
    
    # 验证分页
    content_slides = [s for s in result if s["type"] == "content"]
    print(f"✓ 自动分页: {len(content_slides)} 页内容")
    
    # 验证要点数
    for i, slide in enumerate(content_slides):
        assert len(slide["points"]) <= MAX_POINTS, f"页{i}要点过多: {len(slide['points'])}"
        for j, point in enumerate(slide["points"]):
            assert len(point) <= MAX_POINT_LEN, f"页{i}要点{j}过长: {len(point)}"
    print(f"✓ 所有要点符合长度限制 (≤{MAX_POINT_LEN}字)")
    
    # 验证总页数
    assert len(result) <= 10, f"总页数超限: {len(result)}"
    print(f"✓ 总页数: {len(result)} (≤10)")
    
    return True

def test_scoring():
    """测试评分"""
    print("\n=== Testing Quality Scoring ===")
    
    good_slides = [
        {"type": "content", "title": "标题1", "points": ["短句1", "短句2", "短句3"]},
        {"type": "content", "title": "标题2", "points": ["点1", "点2"]},
    ]
    good_score = score_slides(good_slides)
    print(f"高质量内容得分: {good_score}")
    assert good_score >= 80, f"高质量应该得高分: {good_score}"
    
    bad_slides = [
        {"type": "content", "title": "标题", "points": []},
        {"type": "content", "title": "标题", "points": ["p" * 50]},
    ]
    bad_score = score_slides(bad_slides)
    print(f"低质量内容得分: {bad_score}")
    assert bad_score < 60, f"低质量应该得低分: {bad_score}"
    
    print("✓ 评分系统工作正常")
    return True

def test_rewrite():
    """测试内容重写"""
    print("\n=== Testing Content Rewrite ===")
    
    # 测试替换
    result = rewrite_point("因为成本太高了")
    assert "原因：" in result, f"替换失败: {result}"
    print(f"✓ 替换测试: '因为' → '原因：'")
    
    # 测试截断
    long_text = "这是一个超过20个字符的长句子需要截断"
    result = rewrite_point(long_text)
    assert len(result) <= MAX_POINT_LEN, f"截断失败: {len(result)}"
    print(f"✓ 截断测试: {len(long_text)}字 → {len(result)}字")
    
    # 测试标点清理
    text = "你好，世界。"
    result = rewrite_point(text)
    assert "，" not in result and "。" not in result, "标点清理失败"
    print(f"✓ 标点清理: {text} → {result}")
    
    return True

def run_all_tests():
    print("🔬 Presento Rule Engine Tests\n")
    
    tests = [
        ("Rule Enforcement", test_rule_enforcement),
        ("Quality Scoring", test_scoring),
        ("Content Rewrite", test_rewrite),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {name} passed\n")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} failed: {e}\n")
    
    print("="*50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
