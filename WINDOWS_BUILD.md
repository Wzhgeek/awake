# Windows平台构建说明

## 准备工作

### 1. 获取Windows版本的唤醒词模型文件

目前项目中只包含Linux版本的唤醒词模型文件（`迈灵迈灵_zh_linux_v3_0_0.ppn`）。要在Windows上运行，你需要：

1. 访问 [Picovoice Console](https://console.picovoice.ai/)
2. 登录你的账户
3. 创建一个新的唤醒词模型：
   - 选择语言：中文（Chinese）
   - 输入唤醒词：迈灵迈灵
   - 选择目标平台：Windows
   - 训练模型
4. 下载生成的 `.ppn` 文件
5. 将文件重命名为 `迈灵迈灵_zh_windows_v3_0_0.ppn`
6. 将文件放置在项目根目录

### 2. 确保所有必需文件都存在

在构建之前，确保以下文件都在项目根目录：
- `wake_word_detector.py` - 主程序文件
- `porcupine_params_zh.pv` - 中文语言模型（已包含）
- `迈灵迈灵_zh_windows_v3_0_0.ppn` - Windows版本的唤醒词模型（需要你创建）
- `requirements.txt` - Python依赖列表
- `awake.spec` - PyInstaller配置文件

## 使用GitHub Actions自动构建

### 1. Fork或克隆仓库

```bash
git clone <your-repo-url>
cd awake
```

### 2. 添加Windows模型文件

将你创建的Windows版本模型文件添加到仓库：

```bash
# 将模型文件复制到项目目录
cp path/to/your/迈灵迈灵_zh_windows_v3_0_0.ppn .

# 添加到Git
git add 迈灵迈灵_zh_windows_v3_0_0.ppn
git commit -m "Add Windows wake word model"
```

### 3. 推送到GitHub触发构建

```bash
git push origin main
```

推送后，GitHub Actions会自动：
1. 设置Windows构建环境
2. 安装Python依赖
3. 使用PyInstaller打包成单个可执行文件
4. 创建Release并上传可执行文件

### 4. 下载可执行文件

构建完成后，你可以在以下位置找到可执行文件：
- **GitHub Actions产物**：在Actions标签页找到最新的工作流运行，下载 `awake-windows.exe`
- **Releases页面**：自动创建的Release中会包含 `awake-windows.exe`

## 本地构建（可选）

如果你想在本地构建，可以运行：

```bash
# 安装依赖
pip install -r requirements.txt

# 使用PyInstaller构建
pyinstaller awake.spec --distpath dist --workpath build --clean

# 可执行文件将在 dist/awake.exe
```

## 注意事项

1. **模型兼容性**：确保使用正确平台的模型文件。Linux模型不能在Windows上使用。
2. **访问密钥**：当前代码中已包含访问密钥，但建议你使用自己的密钥。
3. **麦克风权限**：首次运行时，Windows可能会要求麦克风访问权限。

## 故障排除

### 问题：找不到模型文件
- 确保模型文件名称正确：`迈灵迈灵_zh_windows_v3_0_0.ppn`
- 确保文件在项目根目录

### 问题：构建失败
- 检查GitHub Actions日志
- 确保所有依赖都在 `requirements.txt` 中
- 确保 `awake.spec` 配置正确

### 问题：运行时错误
- 确保使用了正确的Windows版本模型
- 检查麦克风权限
- 确保音频设备正常工作 