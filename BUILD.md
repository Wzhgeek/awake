# 🏗️ 构建说明

本文档介绍如何构建离线唤醒词检测系统的可执行文件。

## 📋 目录

- [GitHub Actions自动化构建](#github-actions自动化构建)
- [本地构建](#本地构建)
- [构建文件说明](#构建文件说明)
- [故障排除](#故障排除)

## 🤖 GitHub Actions自动化构建

### 触发条件

GitHub Actions会在以下情况下自动构建：

1. **推送代码到main分支** - 构建但不发布
2. **创建Pull Request** - 构建测试
3. **推送标签** (格式：`v*`) - 构建并发布Release
4. **手动触发** - 在GitHub网页上手动运行

### 创建Release

要创建一个正式发布版本：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

这将自动：
- 构建Windows、Linux、macOS三个平台的可执行文件
- 创建GitHub Release
- 上传所有可执行文件作为Release资产

### 支持的平台

| 平台 | 可执行文件名 | 说明 |
|------|-------------|------|
| Windows | `awake-windows.exe` | 双击运行 |
| Linux | `awake-linux` | 需要添加执行权限 |
| macOS | `awake-macos` | 需要添加执行权限 |

## 🖥️ 本地构建

### 前置要求

1. **Python 3.8+**
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **系统依赖**：
   - **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
   - **CentOS/RHEL**: `sudo yum install portaudio-devel`
   - **macOS**: `brew install portaudio`
   - **Windows**: 通常不需要额外安装

### 快速构建

使用提供的构建脚本：

```bash
python build_local.py
```

### 手动构建

如果您想手动控制构建过程：

```bash
# 清理之前的构建
rm -rf dist build

# 使用PyInstaller构建
pyinstaller awake.spec --clean

# 查看构建结果
ls -la dist/
```

### 构建结果

构建成功后，可执行文件将位于 `dist/` 目录中：

```
dist/
├── awake-windows.exe    # Windows版本
├── awake-linux          # Linux版本
└── awake-macos          # macOS版本
```

## 📁 构建文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `awake.spec` | PyInstaller配置文件，定义打包参数 |
| `build_local.py` | 本地构建脚本，包含依赖检查和构建流程 |
| `.github/workflows/build-executable.yml` | GitHub Actions工作流配置 |

### awake.spec 配置

```python
# 自动收集pvporcupine的数据文件
porcupine_datas = collect_data_files('pvporcupine')

# 添加项目模型文件
datas = [
    ('porcupine_params_zh.pv', '.'),
    ('迈灵迈灵_zh_linux_v3_0_0.ppn', '.')
]
```

### 包含的资源文件

构建的可执行文件会自动包含：
- `porcupine_params_zh.pv` - 中文语言模型
- `迈灵迈灵_zh_linux_v3_0_0.ppn` - 自定义唤醒词模型
- pvporcupine库的相关数据文件

## 🔧 故障排除

### 常见问题

1. **PyAudio安装失败**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev python3-pyaudio
   
   # CentOS/RHEL  
   sudo yum install portaudio-devel
   
   # macOS
   brew install portaudio
   ```

2. **模型文件缺失**
   - 确保 `porcupine_params_zh.pv` 和 `迈灵迈灵_zh_linux_v3_0_0.ppn` 在项目根目录
   - 检查文件是否损坏（可以用 `file` 命令检查）

3. **权限问题** (Linux/macOS)
   ```bash
   chmod +x dist/awake-linux    # Linux
   chmod +x dist/awake-macos    # macOS
   ```

4. **macOS安全提示**
   - 系统偏好设置 → 安全性与隐私 → 通用 → 点击"仍要打开"

### 调试构建问题

1. **检查依赖**：
   ```bash
   python build_local.py  # 会自动检查所有依赖
   ```

2. **详细构建日志**：
   ```bash
   pyinstaller awake.spec --clean --log-level DEBUG
   ```

3. **测试可执行文件**：
   ```bash
   # 在dist目录中直接运行
   ./dist/awake-linux --help  # 查看是否能正常启动
   ```

### GitHub Actions问题

1. **查看构建日志**：在GitHub仓库的Actions标签页查看详细日志

2. **本地测试**：先在本地成功构建后再推送

3. **依赖问题**：确保 `requirements.txt` 包含所有必要依赖

## 💡 最佳实践

1. **版本管理**：使用语义化版本标签（如 `v1.0.0`）
2. **测试先行**：推送前先本地构建测试
3. **文档更新**：重大更新时同步更新README
4. **资源优化**：定期检查可执行文件大小，优化不必要的依赖

## 🔗 相关链接

- [PyInstaller文档](https://pyinstaller.readthedocs.io/)
- [GitHub Actions文档](https://docs.github.com/cn/actions)
- [Porcupine文档](https://picovoice.ai/docs/porcupine/) 