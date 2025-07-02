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
python main.py --query "cat" --output ./output --max_results 10
```

- `--query`：图片搜索关键词（必填）
- `--output`：图片保存路径（必填）
- `--max_results`：采集图片最大数量（可选，默认10）

## 目录结构

- `main.py`：主程序入口
- `src/`：核心代码
- `requirements.txt`：依赖包列表
- `.gitignore`：Git忽略文件

## 说明

- 支持多种搜索引擎，具体可在 `src/config` 中配置。
- 采集到的图片将保存在指定目录下。 