# awake

# 离线唤醒词检测系统 (Awake)

基于 Porcupine 引擎的离线中文唤醒词检测程序，支持"迈灵迈灵"唤醒词。

## 特性

- 🎯 完全离线运行，无需网络连接
- 🗣️ 支持中文唤醒词"迈灵迈灵"
- ⚡ 低延迟，实时响应
- 💻 跨平台支持（Windows/Linux/Mac）
- 📦 提供预编译的可执行文件

## 快速开始

### 下载预编译版本

访问 [Releases](../../releases) 页面下载最新版本的可执行文件：
- Windows: `awake-windows.exe`

### 运行程序

1. 双击运行下载的可执行文件
2. 对着麦克风说"迈灵迈灵"
3. 程序检测到唤醒词后会输出：`{"awake": true}`

## 从源码构建

### 环境要求

- Python 3.8+
- 麦克风设备
- Porcupine访问密钥（可从[Picovoice Console](https://console.picovoice.ai/)免费获取）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python wake_word_detector.py
```

## Windows平台构建

如需为Windows平台构建可执行文件，请参阅 [WINDOWS_BUILD.md](WINDOWS_BUILD.md)。

## 项目结构

```
awake/
├── wake_word_detector.py    # 主程序
├── requirements.txt         # Python依赖
├── awake.spec              # PyInstaller配置
├── porcupine_params_zh.pv  # 中文语言模型
├── 迈灵迈灵_zh_linux_v3_0_0.ppn  # Linux唤醒词模型
└── .github/
    └── workflows/
        └── build-executable.yml  # GitHub Actions构建配置
```

## 开发说明

### 添加新的唤醒词

1. 在 [Picovoice Console](https://console.picovoice.ai/) 创建新的唤醒词模型
2. 下载对应平台的 `.ppn` 文件
3. 修改 `wake_word_detector.py` 中的 `keywords_config` 配置

### 本地构建可执行文件

```bash
pyinstaller awake.spec --distpath dist --workpath build --clean
```

## 许可证

本项目使用 Porcupine 引擎，请遵守相关许可条款。

## 致谢

- [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) - 提供离线唤醒词检测引擎