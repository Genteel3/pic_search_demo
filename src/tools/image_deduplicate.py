import os
from PIL import Image
import imagehash

# 中文注释：对指定文件夹中的图片进行去重，保留每组重复图片中的第一张

def deduplicate_images(folder_path):
    """
    对文件夹中的图片使用感知哈希去重，保留每组重复图片中的第一张。
    :param folder_path: 图片文件夹路径
    :return: 去重后保留的图片数量
    """
    hash_dict = {}
    removed_count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue
        try:
            with Image.open(file_path) as img:
                img_hash = str(imagehash.phash(img))
            if img_hash in hash_dict:
                os.remove(file_path)
                removed_count += 1
                print(f"已删除重复图片: {file_path}")
            else:
                hash_dict[img_hash] = file_path
        except Exception as e:
            print(f"处理图片失败: {file_path}, 错误: {e}")
    print(f"去重完成，保留图片数量: {len(hash_dict)}，删除图片数量: {removed_count}")
    return len(hash_dict) 