import argparse
import os
from src.tools.search import get_web_search_tool
from src.tools.image_deduplicate import deduplicate_images

from dotenv import load_dotenv
load_dotenv()

# 主程序入口
if __name__ == "__main__":
  
    parser = argparse.ArgumentParser(description="图片采集工具")
    parser.add_argument('--query', type=str, required=True, help='图片搜索关键词')
    parser.add_argument('--output', type=str, required=True, help='图片保存路径')
    parser.add_argument('--max_results', type=int, default=10, help='采集图片的最大数量')
    args = parser.parse_args()

    # 创建保存目录
    os.makedirs(args.output, exist_ok=True)

    # 获取搜索工具
    search_tool = get_web_search_tool(args.max_results)
    # 执行搜索
    results = search_tool.run(args.query)

    # print('===============================================')

    # # 保存搜索结果到TXT文件
    # result_txt_path = os.path.join(args.output, "result.txt")
    # with open(result_txt_path, 'w', encoding='utf-8') as f:
    #     f.write(str(results))
    # print(f"搜索结果已保存到: {result_txt_path}")


    # 在搜索结果中只保留'type'为'image'的字典元素
    image_dicts = [item for item in results if isinstance(item, dict) and item.get('type') == 'image']

    image_count = 0
    for img in image_dicts:
        url = img.get('image_url')
        if not url:
            continue
        try:
            import requests
            img_data = requests.get(url, timeout=10).content
            img_ext = os.path.splitext(url)[-1] or '.jpg'
            img_path = os.path.join(args.output, f"{image_count+1}{img_ext}")
            with open(img_path, 'wb') as f:
                f.write(img_data)
            image_count += 1
            print(f"已保存: {img_path}")
            if image_count >= args.max_results:
                break
        except Exception as e:
            print(f"下载失败: {url}, 错误: {e}")

    print(f"共采集图片: {image_count} 张")

    # 对保存目录进行图片去重
    deduplicate_images(args.output) 