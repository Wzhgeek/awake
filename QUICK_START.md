# 快速开始指南 - GitHub Actions自动打包发布

## 前置要求

1. 一个GitHub账号
2. 将此项目上传到你的GitHub仓库

## 自动打包发布步骤

### 1. 准备模型文件（重要！）

由于项目中只包含Linux版本的唤醒词模型，你需要为Windows准备相应的模型文件：

**选项A：创建Windows模型（推荐）**
- 访问 [Picovoice Console](https://console.picovoice.ai/)
- 创建"迈灵迈灵"的Windows版本模型
- 下载并重命名为 `迈灵迈灵_zh_windows_v3_0_0.ppn`
- 将文件添加到项目根目录

**选项B：使用现有Linux模型（可能有兼容性问题）**
- 程序会自动尝试使用现有的Linux模型文件
- 但这可能导致在Windows上运行时出现问题

### 2. 推送代码触发构建

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "准备Windows构建"

# 推送到main分支
git push origin main
```

### 3. 查看构建进度

1. 打开你的GitHub仓库
2. 点击 "Actions" 标签
3. 你会看到 "构建可执行文件" 工作流正在运行
4. 点击进入查看详细日志

### 4. 获取构建产物

构建成功后，有两种方式获取可执行文件：

**方式一：从Actions下载（临时）**
- 在Actions运行页面
- 找到 "Artifacts" 部分
- 下载 `awake-windows.exe`

**方式二：从Releases下载（永久）**
- 转到仓库的 "Releases" 页面
- 找到最新的发布版本
- 下载 `awake-windows.exe`

## 创建正式版本发布

如果你想创建一个正式的版本发布：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

这会触发工作流创建一个正式的GitHub Release。

## 故障排除

### 构建失败？
1. 检查Actions日志中的错误信息
2. 确保所有必需文件都存在
3. 确保requirements.txt中的依赖都正确

### 可执行文件运行错误？
1. 确保使用了正确平台的模型文件
2. 检查是否有杀毒软件误报
3. 确保有麦克风权限

### 找不到Release？
- 只有推送到main分支或创建标签时才会创建Release
- 检查Actions是否成功完成

## 测试可执行文件

下载 `awake-windows.exe` 后：
1. 双击运行
2. 对麦克风说"迈灵迈灵"
3. 看到输出 `{"awake": true}` 表示成功

## 下一步

- 查看 [README.md](README.md) 了解更多功能
- 查看 [WINDOWS_BUILD.md](WINDOWS_BUILD.md) 了解本地构建方法
- 修改 `wake_word_detector.py` 添加自定义功能 