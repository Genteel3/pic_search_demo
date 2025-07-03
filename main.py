import argparse
import os
from src.tools.search import get_web_search_tool
from src.tools.image_deduplicate import deduplicate_images
from urllib.parse import urlparse
import json

from dotenv import load_dotenv
load_dotenv()

# 主程序入口
if __name__ == "__main__":
  
    parser = argparse.ArgumentParser(description="图片采集工具")
    parser.add_argument('--query', type=str, required=True, help='图片搜索关键词')
    parser.add_argument('--output', type=str, required=True, help='图片保存路径')
    args = parser.parse_args()

    # 创建保存目录
    os.makedirs(args.output, exist_ok=True)

    # 获取搜索工具
    search_tool = get_web_search_tool()
    # 执行搜索
    results = search_tool.run(args.query)

    # print('===============================================')

    # # 保存搜索结果到json文件
    # result_json_path = os.path.join(args.output, "result.json")
    # with open(result_json_path, 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)
    # print(f"搜索结果已保存到: {result_json_path}")


    # 在搜索结果中只保留'type'为'image'的字典元素
    image_dicts = [item for item in results if isinstance(item, dict) and item.get('type') == 'image']

    def get_image_extension(url):
        """从URL中提取图片扩展名，若无则默认.jpg"""
        path = urlparse(url).path
        ext = os.path.splitext(path)[-1]
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            ext = '.jpg'
        return ext

    image_count = 0
    for img in image_dicts:
        url = img.get('image_url')
        if not url:
            continue
        try:
            import requests
            resp = requests.get(url, timeout=10)
            # 检查响应状态码和Content-Type，确保是图片
            if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
                img_ext = get_image_extension(url)
                img_path = os.path.join(args.output, f"{image_count+1}{img_ext}")
                with open(img_path, 'wb') as f:
                    f.write(resp.content)
                image_count += 1
                print(f"已保存: {img_path}")
            else:
                print(f"下载失败: {url}, 非图片或状态码异常")
        except Exception as e:
            print(f"下载失败: {url}, 错误: {e}")

    print(f"共采集图片: {image_count} 张")

    # 对保存目录进行图片去重
    deduplicate_images(args.output) 