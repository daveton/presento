#!/usr/bin/env python3
"""
检查文件大小
- 单文件不超过 400 行
- 警告：超过 300 行
"""

import os

MAX_LINES = 400
WARNING_LINES = 300

def check_file_sizes():
    """检查所有 Python 文件大小"""
    violations = []
    warnings = []
    
    for root, dirs, files in os.walk('backend'):
        # 跳过非项目文件
        if '__pycache__' in root or '.git' in root:
            continue
        
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                if lines > MAX_LINES:
                    violations.append(
                        f"[FILE TOO LARGE] {filepath}: {lines} lines "
                        f"(max {MAX_LINES})"
                    )
                elif lines > WARNING_LINES:
                    warnings.append(
                        f"[WARNING] {filepath}: {lines} lines "
                        f"(consider splitting at {MAX_LINES})"
                    )
    
    return violations, warnings

def run_check():
    """运行文件大小检查"""
    violations, warnings = check_file_sizes()
    
    # 打印警告但不阻止
    for warning in warnings:
        print(warning)
    
    return violations

if __name__ == '__main__':
    violations = run_check()
    if violations:
        print("\n".join(violations))
        exit(1)
    else:
        print("✅ File size check passed")
