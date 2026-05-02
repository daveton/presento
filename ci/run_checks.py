#!/usr/bin/env python3
"""
CI 入口 - 运行所有检查
"""

import sys
import importlib.util

def run_all_checks():
    """运行所有检查脚本"""
    all_violations = []
    
    checks = [
        ('Architecture', 'check_architecture'),
        ('Pipeline', 'check_pipeline'),
        ('File Size', 'check_file_size'),
        ('Forbidden Imports', 'check_forbidden_imports'),
    ]
    
    print("🔍 Running Presento CI checks...\n")
    
    for name, module_name in checks:
        print(f"Running {name} check...")
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, 
                f"ci/{module_name}.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            violations = module.run_check()
            all_violations.extend(violations)
            
        except Exception as e:
            print(f"⚠️  Check {name} failed to run: {e}")
    
    print("\n" + "="*50)
    
    if all_violations:
        print(f"❌ {len(all_violations)} violation(s) found:\n")
        for v in all_violations:
            print(f"  • {v}")
        print("\n🚫 Commit blocked by CI rules")
        return False
    else:
        print("✅ All checks passed!")
        return True

if __name__ == '__main__':
    success = run_all_checks()
    sys.exit(0 if success else 1)
