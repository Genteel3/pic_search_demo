# 图片采集工具

本项目实现了基于多种搜索引擎和大模型优化的图片采集功能，支持命令行参数自定义搜索关键词、图片保存路径和图片数量上限。

## 环境依赖

- Python 3.8+
- 依赖包见 `requirements.txt`
- 需注册并获取 DashScope（通义千问）API KEY

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置API KEY

请在运行前设置环境变量 `DASHSCOPE_API_KEY`，例如：

- Windows PowerShell:
  ```powershell
  $env:DASHSCOPE_API_KEY="你的apikey"
  ```
- Windows CMD:
  ```cmd
  set DASHSCOPE_API_KEY=你的apikey
  ```
- Linux/macOS:
  ```bash
  export DASHSCOPE_API_KEY=你的apikey
  ```

## 使用方法

```bash
python main.py --query "cat" --output ./output --max_images 10
```

- `--query`：图片搜索关键词（必填）
- `--output`：图片保存路径（必填）
- `--max_images`：图片生成的上限数量（可选，默认10）

## 功能说明

- 输入查询图片的文字，调用大模型（Qwen-turbo-latest）自动生成10个优化后的图片描述。
- 用这些描述分别去搜索图片，累计下载，超过上限即停止。
- 支持多种搜索引擎，图片自动去重。

## 目录结构

- `main.py`
- `src/llm/qwen_turbo.py`  # 大模型API调用与描述优化
- `src/prompt/Prompt.py`   # 大模型Prompt模板