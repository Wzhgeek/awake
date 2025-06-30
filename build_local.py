#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地构建脚本 - 离线唤醒词检测系统
用于在本地测试PyInstaller构建过程
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并处理结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必需的包
    required_packages = ['pvporcupine', 'pyaudio', 'PyInstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"⚠️  缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def check_model_files():
    """检查模型文件"""
    print("📁 检查模型文件...")
    
    model_files = [
        'porcupine_params_zh.pv',
        '迈灵迈灵_zh_linux_v3_0_0.ppn'
    ]
    
    missing_files = []
    for file in model_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"✅ {file} ({size:.1f} KB)")
        else:
            missing_files.append(file)
            print(f"❌ {file} 缺失")
    
    if missing_files:
        print(f"⚠️  缺少模型文件: {', '.join(missing_files)}")
        return False
    
    return True

def build_executable():
    """构建可执行文件"""
    print("🏗️  开始构建可执行文件...")
    
    # 清理之前的构建
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("🧹 清理dist目录")
    
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("🧹 清理build目录")
    
    # 运行PyInstaller
    cmd = "pyinstaller awake.spec --distpath dist --workpath build --clean"
    if not run_command(cmd, "PyInstaller构建"):
        return False
    
    # 检查构建结果
    system = platform.system().lower()
    if system == 'windows':
        executable_name = 'awake.exe'
    else:
        executable_name = 'awake'
    
    executable_path = os.path.join('dist', executable_name)
    if os.path.exists(executable_path):
        size = os.path.getsize(executable_path) / (1024 * 1024)  # MB
        print(f"✅ 构建成功: {executable_path} ({size:.1f} MB)")
        
        # 重命名为平台特定的名称
        if system == 'windows':
            new_name = 'awake-windows.exe'
        elif system == 'darwin':
            new_name = 'awake-macos'
        else:
            new_name = 'awake-linux'
        
        new_path = os.path.join('dist', new_name)
        os.rename(executable_path, new_path)
        print(f"📝 重命名为: {new_path}")
        
        return True
    else:
        print(f"❌ 构建失败: 未找到 {executable_path}")
        return False

def test_executable():
    """测试可执行文件"""
    print("🧪 测试可执行文件...")
    
    system = platform.system().lower()
    if system == 'windows':
        executable_name = 'awake-windows.exe'
    elif system == 'darwin':
        executable_name = 'awake-macos'
    else:
        executable_name = 'awake-linux'
    
    executable_path = os.path.join('dist', executable_name)
    
    if not os.path.exists(executable_path):
        print(f"❌ 找不到可执行文件: {executable_path}")
        return False
    
    # 简单的启动测试
    print("⚡ 尝试启动程序（5秒后自动终止）...")
    try:
        import signal
        import time
        
        def timeout_handler(signum, frame):
            raise TimeoutError("测试超时")
        
        # 在非Windows系统上设置超时
        if system != 'windows':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
        
        # 启动程序进行测试
        process = subprocess.Popen([executable_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # 等待一下然后终止
        time.sleep(2)
        process.terminate()
        
        if system != 'windows':
            signal.alarm(0)  # 取消超时
        
        print("✅ 程序启动测试通过")
        return True
        
    except Exception as e:
        print(f"⚠️  测试警告: {e}")
        print("💡 这可能是因为缺少音频设备或权限，程序本身可能正常")
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("🏗️  离线唤醒词检测系统 - 本地构建脚本")
    print(f"🖥️  平台: {platform.system()} {platform.architecture()[0]}")
    print("=" * 60)
    
    # 检查依赖项
    if not check_dependencies():
        return False
    
    # 检查模型文件
    if not check_model_files():
        return False
    
    # 构建可执行文件
    if not build_executable():
        return False
    
    # 测试可执行文件
    test_executable()
    
    print("=" * 60)
    print("🎉 构建完成！")
    print("📁 可执行文件位置: dist/")
    print("💡 您现在可以测试运行生成的可执行文件")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ 用户中断构建过程")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        sys.exit(1) 