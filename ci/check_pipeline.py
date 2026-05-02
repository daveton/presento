#!/usr/bin/env python3
"""
检查 Pipeline 完整性
- 是否跳过了必要步骤
"""

import os
import re

def check_pipeline_completeness():
    """检查 pipeline.py 是否包含所有必要步骤"""
    violations = []
    
    pipeline_file = "backend/core/pipeline.py"
    
    if not os.path.exists(pipeline_file):
        violations.append("[MISSING] core/pipeline.py not found")
        return violations
    
    with open(pipeline_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pipeline 必须包含的步骤
    required_steps = [
        ('parse', ['parse']),
        ('extract', ['extract']),
        ('rewrite', ['rewrite']),
        ('rules', ['enforce_rules', 'rules']),
        ('render', ['render', 'create_ppt']),
    ]
    
    for step_name, keywords in required_steps:
        found = any(kw in content.lower() for kw in keywords)
        if not found:
            violations.append(
                f"[PIPELINE INCOMPLETE] Missing step: {step_name}"
            )
    
    return violations

def check_step_order():
    """检查步骤顺序（简单检查）"""
    violations = []
    
    pipeline_file = "backend/core/pipeline.py"
    
    if not os.path.exists(pipeline_file):
        return violations
    
    with open(pipeline_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # rules 必须在 render 之前
    rules_pos = content.lower().find('enforce_rules')
    render_pos = content.lower().find('render')
    
    if rules_pos != -1 and render_pos != -1:
        if rules_pos > render_pos:
            violations.append(
                "[PIPELINE ORDER] rules must come before render"
            )
    
    return violations

def run_check():
    """运行 Pipeline 检查"""
    violations = []
    violations.extend(check_pipeline_completeness())
    violations.extend(check_step_order())
    
    return violations

if __name__ == '__main__':
    violations = run_check()
    if violations:
        print("\n".join(violations))
        exit(1)
    else:
        print("✅ Pipeline check passed")
