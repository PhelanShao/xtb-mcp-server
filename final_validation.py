#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTB MCP服务器最终验证脚本
验证项目是否准备好上线部署
"""

import sys
import os
from pathlib import Path
import importlib.util

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if Path(filepath).exists():
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[FAIL] {description}: {filepath} - 文件不存在")
        return False

def check_directory_structure():
    """检查项目目录结构"""
    print("=== 检查项目目录结构 ===")
    
    required_files = [
        ("main.py", "MCP服务器主入口"),
        ("requirements.txt", "依赖文件"),
        ("DEPLOYMENT_GUIDE.md", "部署指南"),
        ("PROJECT_SUMMARY.md", "项目总结"),
        ("run_tests.py", "测试运行器"),
        ("test_mcp_functionality.py", "MCP功能测试"),
    ]
    
    required_dirs = [
        ("xtb_input_generator", "核心生成器模块"),
        ("resources", "资源文件目录"),
        ("tests", "测试目录"),
    ]
    
    all_good = True
    
    for filepath, desc in required_files:
        if not check_file_exists(filepath, desc):
            all_good = False
    
    for dirpath, desc in required_dirs:
        if Path(dirpath).is_dir():
            print(f"[OK] {desc}: {dirpath}/")
        else:
            print(f"[FAIL] {desc}: {dirpath}/ - 目录不存在")
            all_good = False
    
    return all_good

def check_core_modules():
    """检查核心模块是否可以导入"""
    print("\n=== 检查核心模块导入 ===")
    
    modules_to_check = [
        ("xtb_input_generator", "核心生成器模块"),
        ("xtb_input_generator.generator", "生成器主模块"),
        ("xtb_input_generator.structure_utils", "结构工具模块"),
    ]
    
    all_good = True
    
    for module_name, desc in modules_to_check:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                print(f"[OK] {desc}: {module_name}")
            else:
                print(f"[FAIL] {desc}: {module_name} - 模块未找到")
                all_good = False
        except Exception as e:
            print(f"[FAIL] {desc}: {module_name} - 导入错误: {e}")
            all_good = False
    
    return all_good

def check_resource_files():
    """检查资源文件完整性"""
    print("\n=== 检查资源文件 ===")
    
    resource_files = [
        "resources/templates/singlepoint.xtb_tpl",
        "resources/templates/optimization.xtb_tpl", 
        "resources/templates/frequency.xtb_tpl",
        "resources/templates/scan.xtb_tpl",
        "resources/templates/md.xtb_tpl",
        "resources/parameters/gfn0.md",
        "resources/parameters/gfn1.md",
        "resources/parameters/gfn2.md",
        "resources/formats/input_spec.md",
        "resources/help/faq.md",
    ]
    
    all_good = True
    
    for filepath in resource_files:
        if not check_file_exists(filepath, f"资源文件"):
            all_good = False
    
    return all_good

def check_advanced_templates():
    """检查高级模板文件"""
    print("\n=== 检查高级模板文件 ===")
    
    advanced_templates = [
        "resources/sampling/metadynamics.xtb_tpl",
        "resources/templates/sampling/pathfinder.xtb_tpl",
        "resources/templates/sampling/normal_mode_following.xtb_tpl",
        "resources/templates/wavefunction/orbitals.xtb_tpl",
        "resources/templates/advanced/oniom.xtb_tpl",
        "resources/templates/advanced/spectroscopy_ir.xtb_tpl",
        "resources/templates/advanced/spectroscopy_uv_vis.xtb_tpl",
    ]
    
    all_good = True
    
    for filepath in advanced_templates:
        if not check_file_exists(filepath, f"高级模板"):
            all_good = False
    
    return all_good

def run_basic_functionality_test():
    """运行基本功能测试"""
    print("\n=== 运行基本功能测试 ===")
    
    try:
        # 尝试导入并初始化生成器
        from xtb_input_generator import XTBInputGenerator
        generator = XTBInputGenerator()
        print("[OK] XTBInputGenerator初始化成功")
        
        # 测试基本资源访问
        template = generator.get_mcp_resource("xtb://templates/singlepoint")
        if template:
            print("[OK] 模板资源访问正常")
        else:
            print("[FAIL] 模板资源访问失败")
            return False
        
        # 测试基本输入生成
        water_xyz = """3
Water
O  0.000000  0.000000  0.117300
H  0.000000  0.757200 -0.469200
H  0.000000 -0.757200 -0.469200
"""
        
        result = generator.generate_xtb_input_package(
            molecule_data={
                "format": "xyz",
                "content": water_xyz,
                "charge": 0,
                "multiplicity": 1
            },
            calculation_type="singlepoint",
            method="gfn2",
            settings={"solvent": "h2o"}
        )
        
        if "error" not in result and "structure.xyz" in result:
            print("[OK] 基本输入生成功能正常")
        else:
            print("[FAIL] 基本输入生成功能异常")
            return False
        
        return True
        
    except Exception as e:
        print(f"[FAIL] 基本功能测试失败: {e}")
        return False

def check_test_files():
    """检查测试文件"""
    print("\n=== 检查测试文件 ===")
    
    test_files = [
        "tests/__init__.py",
        "tests/test_structure_utils.py",
        "tests/test_generator.py", 
        "tests/test_mcp_server.py",
    ]
    
    all_good = True
    
    for filepath in test_files:
        if not check_file_exists(filepath, "测试文件"):
            all_good = False
    
    return all_good

def main():
    """主验证函数"""
    print("XTB MCP服务器最终验证")
    print("=" * 50)
    
    checks = [
        ("项目目录结构", check_directory_structure),
        ("核心模块导入", check_core_modules),
        ("资源文件完整性", check_resource_files),
        ("高级模板文件", check_advanced_templates),
        ("测试文件", check_test_files),
        ("基本功能", run_basic_functionality_test),
    ]
    
    all_passed = True
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"[ERROR] {check_name}检查失败: {e}")
            results.append((check_name, False))
            all_passed = False
    
    # 输出总结
    print("\n" + "=" * 50)
    print("验证结果总结:")
    print("-" * 30)
    
    for check_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {check_name}")
    
    print("-" * 30)
    
    if all_passed:
        print("[SUCCESS] 所有验证通过！")
        print("项目已准备好进行部署。")
        print("\n部署步骤:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行测试: python run_tests.py")
        print("3. 功能验证: python test_mcp_functionality.py")
        print("4. 启动服务: python main.py")
        print("5. 参考部署指南: DEPLOYMENT_GUIDE.md")
        return True
    else:
        print("[FAILED] 部分验证失败！")
        print("请修复上述问题后重新验证。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)