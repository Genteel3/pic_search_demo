import os
from dashscope import Generation
from http import HTTPStatus

# 从环境变量加载API KEY
dashscope_api_key = os.getenv('DASHSCOPE_API_KEY')

# 支持模型名参数化，默认使用Qwen-turbo-latest
def rewrite_queries(prompt, n=10, model="qwen-turbo-latest"):
    """
    调用Qwen-turbo大模型重写和优化图片搜索描述。
    prompt: 用户原始输入
    n: 生成描述数量
    model: 使用的大模型名称
    返回：优化后的描述列表
    """
    if not dashscope_api_key:
        raise ValueError("DASHSCOPE_API_KEY未设置")
    from dashscope import api_key
    api_key = dashscope_api_key
    # 构造prompt，要求生成n个不同的图片描述
    full_prompt = f"请根据以下描述，生成{n}个不同但相关、适合图片搜索的中文描述，每个描述一行输出：{prompt}"
    responses = Generation.call(model=model, prompt=full_prompt)
    if responses.status_code == HTTPStatus.OK:
        # 兼容dashscope新版返回结构
        output = responses.output
        # 1. 如果有text属性，取text
        if hasattr(output, "text"):
            text = output.text
        # 2. 如果本身是字符串
        elif isinstance(output, str):
            text = output
        # 3. 其他情况报错
        else:
            raise RuntimeError(f"Qwen-turbo返回内容异常，output类型为{type(output)}，内容为：{output}")
        # 分割并去除空行
        return [line.strip() for line in text.split('\n') if line.strip()]
    else:
        raise RuntimeError(f"Qwen-turbo调用失败: {responses.message}")

if __name__ == "__main__":
    # 测试用例：调用大模型生成图片搜索描述
    test_prompt = "一只可爱的橘猫在花园里玩耍"
    try:
        results = rewrite_queries(test_prompt, n=5)
        print("大模型生成的图片搜索描述：")
        for idx, desc in enumerate(results, 1):
            print(f"{idx}. {desc}")
    except Exception as e:
        print(f"测试失败: {e}") 