#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线唤醒词检测程序
使用Porcupine实现"迈灵迈灵"唤醒词检测
"""

import os
import sys
import struct
import pyaudio
import pvporcupine
from threading import Thread
import time
import json

class WakeWordDetector:
    def __init__(self):
        """初始化唤醒词检测器"""
        self.is_running = False
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        
        # Porcupine访问密钥 - 您需要从Picovoice官网获取免费的访问密钥
        # 请访问 https://console.picovoice.ai/ 注册并获取访问密钥
        # self.access_key = "umxBFGL4+LwwwydBgShOv9d9sY2jlk3YQlrjS93wVkMjXbyU8G/XMw=="  # 请替换为您的实际访问密钥
        self.access_key = "YFQbRTufWcMpXnZ2vpiIQFjnG2Ul3vCntVxambYszRDFh2mmjCH0ZQ=="  # 请替换为您的实际访问密钥
        
        # 自定义关键词模型配置
        self.keywords_config = [
            {
                "name": "迈灵迈灵",
                "model_path": "迈灵迈灵_zh_windows_v3_0_0.ppn",
                "action": "wake_up"
            }
        ]
        
        # 中文语言模型路径
        self.zh_model_path = "porcupine_params_zh.pv"
        
    def initialize_porcupine(self):
        """初始化Porcupine引擎"""
        try:
            # 检查中文语言模型文件是否存在
            if not os.path.exists(self.zh_model_path):
                print(f"❌ 中文模型文件不存在: {self.zh_model_path}")
                print(" 请运行以下命令下载中文模型:")
                print("   wget https://github.com/Picovoice/porcupine/raw/master/lib/common/porcupine_params_zh.pv")
                return False
            
            # 检查所有关键词模型文件是否存在
            keyword_paths = []
            missing_files = []
            
            for config in self.keywords_config:
                if os.path.exists(config["model_path"]):
                    keyword_paths.append(config["model_path"])
                    print(f"✅ 找到关键词模型: {config['name']} ({config['model_path']})")
                else:
                    missing_files.append(config)
            
            if missing_files:
                print("⚠️  以下关键词模型文件缺失:")
                for config in missing_files:
                    print(f"   - {config['name']}: {config['model_path']}")
                print(" 请在 Picovoice Console 创建相应的关键词模型")
                
                # 如果至少有一个模型文件，继续运行，否则退出
                if not keyword_paths:
                    return False
                else:
                    print(" 将使用可用的关键词模型继续运行...")
                    # 更新配置，只保留存在的模型
                    self.keywords_config = [config for config in self.keywords_config 
                                          if os.path.exists(config["model_path"])]
            
            # 使用中文模型文件和关键词文件创建Porcupine实例
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=keyword_paths,
                model_path=self.zh_model_path
            )
            
            print(f"✅ Porcupine初始化成功!")
            print(f" 支持的唤醒词: {', '.join([config['name'] for config in self.keywords_config])}")
            print(f" 采样率: {self.porcupine.sample_rate} Hz")
            print(f"️ 帧长度: {self.porcupine.frame_length}")
            print(f" 使用语言模型: {self.zh_model_path}")
            return True
        except Exception as e:
            print(f"❌ Porcupine初始化失败: {e}")
            print(" 请确保访问密钥正确且所有模型文件都存在")
            return False
    
    def initialize_audio(self):
        """初始化音频流"""
        try:
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            print(" 音频流初始化成功!")
            return True
        except Exception as e:
            print(f"❌ 音频流初始化失败: {e}")
            return False
    
    def detect_wake_word(self):
        """检测唤醒词的主循环"""
        print(" 开始监听唤醒词...")
        print(" 可用命令:")
        print(f"   - 说出 '迈灵迈灵' → 输出唤醒状态")
        print("⏹️  按Ctrl+C停止程序")
        
        try:
            while self.is_running:
                # 读取音频数据
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # 检测唤醒词
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    detected_config = self.keywords_config[keyword_index]
                    detected_keyword = detected_config['name']
                    
                    print(f" 检测到关键词: {detected_keyword}")
                    
                    # 输出JSON格式的stdout
                    wake_status = {"awake": True}
                    print(json.dumps(wake_status, ensure_ascii=False))
                    
                    print("⚡ 唤醒词检测成功")
                    # 短暂停顿避免重复触发
                    time.sleep(2)
                    print(" 继续监听...")
        except KeyboardInterrupt:
            print("\n 用户中断程序")
        except Exception as e:
            print(f"❌ 检测过程中发生错误: {e}")
    
    def start(self):
        """启动唤醒词检测"""
        print(" 启动离线唤醒词检测系统...")
        
        # 初始化Porcupine
        if not self.initialize_porcupine():
            return False
        
        # 初始化音频
        if not self.initialize_audio():
            return False
        
        # 开始检测
        self.is_running = True
        try:
            self.detect_wake_word()
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """停止检测并清理资源"""
        print(" 停止唤醒词检测...")
        self.is_running = False
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        if self.pa:
            self.pa.terminate()
        
        if self.porcupine:
            self.porcupine.delete()
        
        print("✅ 资源清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print(" 离线唤醒词检测系统")
    print(" 支持的关键词:")
    print("   • 迈灵迈灵 → 唤醒并输出JSON状态")
    print(" 基于Porcupine引擎的离线语音识别")
    print("=" * 60)
    
    # 创建检测器实例
    detector = WakeWordDetector()
    
    # 检查访问密钥
    if detector.access_key == "YOUR_ACCESS_KEY_HERE":
        print("⚠️  警告: 请设置您的Porcupine访问密钥!")
        print(" 步骤:")
        print("   1. 访问 https://console.picovoice.ai/")
        print("   2. 注册账户并获取免费访问密钥")
        print("   3. 在代码中替换 'YOUR_ACCESS_KEY_HERE'")
        print(" 您也可以通过环境变量设置: export PORCUPINE_ACCESS_KEY=your_key")
        
        # 尝试从环境变量获取
        env_key = os.getenv('PORCUPINE_ACCESS_KEY')
        if env_key:
            detector.access_key = env_key
            print("✅ 从环境变量获取到访问密钥")
        else:
            return False
    
    # 启动检测
    return detector.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        sys.exit(1) 