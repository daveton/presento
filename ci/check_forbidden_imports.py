#!/usr/bin/env python3
"""
检查禁止的导入
- 防止直接调用外部 API
- 防止使用被禁用的库
"""

import os
import re

def check_llm_usage():
    """检查是否直接调用 LLM（应该通过 infra/llm）"""
    violations = []
    
    # 禁止在 infra/llm 之外的地方直接调用
    forbidden_patterns = [
        (r'openai\.(Async)?OpenAI', 'Direct OpenAI client usage'),
        (r'ChatCompletion', 'Direct ChatCompletion usage'),
        (r'anthropic', 'Direct Anthropic usage'),
    ]
    
    allowed_paths = ['infra/llm', 'ci/']
    
    for root, dirs, files in os.walk('backend'):
        # 跳过允许的路径
        if any(ap in root for ap in allowed_paths):
            continue
        
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    for pattern, msg in forbidden_patterns:
                        if re.search(pattern, line):
                            violations.append(
                                f"[FORBIDDEN IMPORT] {filepath}:{i} - {msg}. "
                                f"Use infra/llm/client.py instead"
                            )
    
    return violations

def check_other_forbidden():
    """检查其他禁止的库"""
    violations = []
    
    # 项目不允许直接使用的库（必须通过封装）
    forbidden_libs = [
        'requests',  # 应该通过 infra/ 封装
    ]
    
    for root, dirs, files in os.walk('backend'):
        if 'infra' in root:
            continue
        
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for lib in forbidden_libs:
                    if f'import {lib}' in content or f'from {lib}' in content:
                        violations.append(
                            f"[FORBIDDEN] {filepath}: Direct import of '{lib}'. "
                            f"Use infra layer instead"
                        )
    
    return violations

def run_check():
    """运行禁止导入检查"""
    violations = []
    violations.extend(check_llm_usage())
    violations.extend(check_other_forbidden())
    
    return violations

if __name__ == '__main__':
    violations = run_check()
    if violations:
        print("\n".join(violations))
        exit(1)
    else:
        print("✅ Forbidden imports check passed")
