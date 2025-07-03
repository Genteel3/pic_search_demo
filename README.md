# 图片采集工具

本项目实现了基于多种搜索引擎的图片采集功能，支持命令行参数自定义搜索关键词和图片保存路径。

## 环境依赖

- Python 3.8+
- 依赖包见 `requirements.txt`

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py --query "cat" --output ./output
```

- `--query`：图片搜索关键词（必填）
- `--output`：图片保存路径（必填）

## 目录结构

- `main.py`