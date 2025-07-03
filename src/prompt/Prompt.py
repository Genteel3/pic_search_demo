# -*- coding: utf-8 -*-
"""
定义大模型生成图片搜索描述的prompt模板
"""

def get_image_search_prompt(user_query, n=10):
    """
    返回用于大模型生成图片搜索描述的prompt
    user_query: 用户原始输入
    n: 生成描述数量
    """

    prompt = f'''你是一个图片搜索专家，擅长根据用户输入的描述生成适合图片搜索的描述。
    请根据以下描述{user_query}，生成{n}个不同但相关、适合图片搜索的描述，每个描述一行输出。
    '''
    return prompt