import argparse
import os
from src.tools.search import get_web_search_tool
from src.tools.image_deduplicate import deduplicate_images
from urllib.parse import urlparse
import json

from dotenv import load_dotenv
load_dotenv()

def get_image_extension(url):
    """从URL中提取图片扩展名，若无则默认.jpg"""
    path = urlparse(url).path
    ext = os.path.splitext(path)[-1]
    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
        ext = '.jpg'
    return ext 


def download_image(url, save_path):
    """并发下载图片"""
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"已保存: {save_path}")
            return True
        else:
            print(f"下载失败: {url}")
            return False
    except Exception as e:
        print(f"下载失败: {url}, 错误: {e}")
        return False

# 主程序入口
if __name__ == "__main__":
  
    parser = argparse.ArgumentParser(description="图片采集工具")
    parser.add_argument('--query', type=str, required=True, help='图片搜索关键词')
    parser.add_argument('--output', type=str, required=True, help='图片保存路径')
    parser.add_argument('--max_images', type=int, default=10, help='图片生成的上限数量，默认为10')
    args = parser.parse_args()

    # 创建保存目录
    os.makedirs(args.output, exist_ok=True)

    # 获取搜索工具
    search_tool = get_web_search_tool()
    # 导入大模型和prompt
    from src.llm.qwen_turbo import rewrite_queries
    from src.prompt.Prompt import get_image_search_prompt
    import concurrent.futures
    import requests

    # 生成优化后的图片搜索描述
    prompt = get_image_search_prompt(args.query, n=args.max_images)
    try:
        rewritten_queries = rewrite_queries(args.query, n=args.max_images)
    except Exception as e:
        print(f"大模型生成描述失败: {e}")
        rewritten_queries = [args.query]

    print('正在进行图片搜索...')


    # 收集所有待下载图片的(url, 保存路径)元组，直到达到max_images*2，允许重复描述采集更多图片
    image_url_path_list = []
    image_url_set = set()  # 用于去重
    image_count = 0
    per_query_limit = 10  # 每个描述最多采集10张图片
    for rewritten_query in rewritten_queries:
        results = search_tool.run(rewritten_query)
        image_dicts = [item for item in results if isinstance(item, dict) and item.get('type') == 'image']
        per_query_count = 0
        for img in image_dicts:
            if image_count >= args.max_images * 2:  # 允许采集更多，后续去重
                break
            url = img.get('image_url')
            if not url or url in image_url_set:
                continue
            img_ext = get_image_extension(url)
            img_path = os.path.join(args.output, f"{image_count+1}{img_ext}")
            image_url_path_list.append((url, img_path))
            image_url_set.add(url)
            image_count += 1
            per_query_count += 1
            if per_query_count >= per_query_limit:
                break
        if image_count >= args.max_images * 2:
            break

    print('图片搜索完成，正在进行图片下载...')

    # 并发下载图片
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda args: download_image(*args), image_url_path_list))
    print(f"共采集图片: {sum(results)} 张")

    # 对保存目录进行图片去重
    deduplicate_images(args.output)

    # 去重后只保留max_images张图片（按文件名排序，保留最新的max_images张）
    all_images = [f for f in os.listdir(args.output) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
    if len(all_images) > args.max_images:
        # 按文件名排序，保留最新的max_images张
        all_images.sort(key=lambda x: int(os.path.splitext(x)[0]))
        to_remove = all_images[:-args.max_images]
        for fname in to_remove:
            try:
                os.remove(os.path.join(args.output, fname))
                print(f"超出上限，已删除: {fname}")
            except Exception as e:
                print(f"删除文件失败: {fname}, 错误: {e}")
        # 更新all_images为剩余图片
        all_images = all_images[-args.max_images:]
    else:
        # 不足max_images时全部保留
        all_images.sort(key=lambda x: int(os.path.splitext(x)[0]))
    # 对保留图片按1,2,3...max_images顺序重命名
    for idx, fname in enumerate(all_images, 1):
        old_path = os.path.join(args.output, fname)
        ext = os.path.splitext(fname)[-1]
        new_name = f"{idx}{ext}"
        new_path = os.path.join(args.output, new_name)
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
                print(f"重命名: {fname} -> {new_name}")
            except Exception as e:
                print(f"重命名失败: {fname} -> {new_name}, 错误: {e}")
    print(f"最终保留图片: {min(len(all_images), args.max_images)} 张，已按顺序重命名。")

