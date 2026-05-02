#!/usr/bin/env python3
"""
Presento 质量测试
验证PPT生成的关键指标
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.renderer import enforce_rules, score_slides, MAX_TITLE_LEN, MAX_POINT_LEN, MAX_POINTS

def test_rule_enforcement():
    """测试规则引擎"""
    print("\n=== Testing Rule Enforcement ===")
    
    # 测试数据：超长标题和要点
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
                "点6",  # 应该被截断
                "点7"   # 应该被截断
            ]
        }
    ]
    
    result = enforce_rules(slides)
    
    # 验证封面标题
    assert len(result[0]["title"]) <= MAX_TITLE_LEN, f"封面标题过长: {len(result[0]['title'])}"
    print(f"✓ 封面标题截断: {result[0]['title']}")
    
    # 验证内容页被分页
    content_slides = [s for s in result if s["type"] == "content"]
    assert len(content_slides) >= 2, "应该自动分页"
    print(f"✓ 自动分页: {len(content_slides)} 页内容")
    
    # 验证每页要点数
    for slide in content_slides:
        assert len(slide["points"]) <= MAX_POINTS, f"要点过多: {len(slide['points'])}"
        for point in slide["points"]:
            assert len(point) <= MAX_POINT_LEN, f"要点过长: {len(point)}"
    print(f"✓ 所有要点符合长度限制")
    
    # 验证总页数
    assert len(result) <= 10, f"总页数超限: {len(result)}"
    print(f"✓ 总页数: {len(result)} (≤10)")
    
    return True

def test_scoring():
    """测试质量评分"""
    print("\n=== Testing Quality Scoring ===")
    
    # 高质量内容
    good_slides = [
        {"type": "content", "title": "标题1", "points": ["短句1", "短句2", "短句3"]},
        {"type": "content", "title": "标题2", "points": ["点1", "点2"]},
    ]
    good_score = score_slides(good_slides)
    print(f"高质量内容得分: {good_score}")
    assert good_score >= 80, f"高质量应该得高分: {good_score}"
    
    # 低质量内容
    bad_slides = [
        {"type": "content", "title": "标题", "points": []},  # 无要点
        {"type": "content", "title": "标题", "points": ["p" * 50]},  # 超长
    ]
    bad_score = score_slides(bad_slides)
    print(f"低质量内容得分: {bad_score}")
    assert bad_score < 60, f"低质量应该得低分: {bad_score}"
    
    print("✓ 评分系统工作正常")
    return True

def test_content_rewrite():
    """测试内容重写"""
    print("\n=== Testing Content Rewrite ===")
    
    from core.renderer import rewrite_point
    
    test_cases = [
        ("因为成本太高了", "原因："),  # 应该替换
        ("这是一个很长的句子超过20个字", None),  # 应该截断
    ]
    
    for input_text, expected in test_cases:
        result = rewrite_point(input_text)
        assert len(result) <= MAX_POINT_LEN, f"截断失败: {len(result)}"
        if expected:
            assert expected in result, f"重写失败: {result}"
    
    print("✓ 内容重写工作正常")
    return True

def run_all_tests():
    """运行所有测试"""
    print("🔬 Presento Quality Tests\n")
    
    tests = [
        ("Rule Enforcement", test_rule_enforcement),
        ("Quality Scoring", test_scoring),
        ("Content Rewrite", test_content_rewrite),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {name} passed")
        except Exception as e:
            failed += 1
            print(f"❌ {name} failed: {e}")
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
