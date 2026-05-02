#!/usr/bin/env python3
"""
检查架构边界
- api/ 层不能包含业务逻辑
- 不能绕过 pipeline 直接调用 renderer
"""

import os
import re

def check_api_layer():
    """检查 api/ 层是否写了业务逻辑"""
    violations = []
    
    api_dir = "backend/api"
    if not os.path.exists(api_dir):
        return []
    
    # 业务逻辑关键词（不应该出现在 api 层）
    forbidden_patterns = [
        r'render_ppt\s*\(',
        r'rewrite_content\s*\(',
        r'enforce_rules\s*\(',
        r'score_ppt\s*\(',
        r'openai\.',
        r'ChatCompletion',
    ]
    
    for filename in os.listdir(api_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(api_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    for pattern in forbidden_patterns:
                        if re.search(pattern, line):
                            violations.append(
                                f"[API VIOLATION] {filename}:{i} contains '{pattern}' - "
                                f"Business logic should be in core/, not api/"
                            )
    
    return violations

def check_pipeline_bypass():
    """检查是否绕过 pipeline 直接调用"""
    violations = []
    
    # 应该只从 pipeline 导入的函数
    pipeline_only = [
        ('core.renderer', 'create_ppt_file'),
        ('infra.llm.client', 'call_llm'),
    ]
    
    for root, dirs, files in os.walk('backend'):
        # 跳过 infra（允许直接调用）
        if 'infra' in root:
            continue
        
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for module, func in pipeline_only:
                    # 检查是否直接导入
                    import_pattern = rf'from\s+{module.replace(".", "\\.")}\s+import\s+{func}'
                    if re.search(import_pattern, content):
                        # 检查是否在 pipeline.py 中
                        if 'pipeline.py' not in filepath:
                            violations.append(
                                f"[BYPASS VIOLATION] {filepath}: "
                                f"Direct import of {func} from {module}. "
                                f"Must go through core.pipeline"
                            )
    
    return violations

def run_check():
    """运行架构检查"""
    violations = []
    violations.extend(check_api_layer())
    violations.extend(check_pipeline_bypass())
    
    return violations

if __name__ == '__main__':
    violations = run_check()
    if violations:
        print("\n".join(violations))
        exit(1)
    else:
        print("✅ Architecture check passed")
