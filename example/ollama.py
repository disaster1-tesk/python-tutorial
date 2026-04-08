import requests
import json


def call_ollama(prompt, model_name="deepseek-r1:8b", n_predict=50, stop=None):
    """
  调用本地 Ollama 服务生成文本

  参数:
  prompt (str): 输入提示
  model_name (str): 模型名称，默认为"llama2"
  n_predict (int): 生成的最大token数
  stop (list): 停止生成的token列表

  返回:
  dict: 包含生成结果的字典
  """
    # Ollama API 的默认端口
    if stop is None:
        stop = ["\n", "###"]
    base_url = "http://localhost:11434/api/generate"

    # 构建请求数据
    payload = {
        "model": model_name,
        "prompt": prompt,
        "n_predict": n_predict,
        "stop": stop,
        "stream": False  # 关闭流式响应，以便一次性获取完整结果
    }

    try:
        # 发送请求
        response = requests.post(
            base_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        # 解析响应
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"API请求失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None


def get_completion(prompt, model_name="qwen2.5-coder:14b"):
    """获取完整的文本生成结果"""
    result = call_ollama(prompt, model_name)

    if result is None:
        return None

    # 构建完整的回复
    full_response = ""
    for i in range(len(result["response"]) + 1):
        if i < len(result["response"]):
            full_response += result["response"][i]

    return full_response


# 使用示例
if __name__ == "__main__":
    # 1. 单次简单查询
    prompt1 = "写一个关于人工智能的短段落。"
    result1 = get_completion(prompt1, model_name="deepseek-r1:8b")

    if result1:
        print("生成结果:")
        print(result1)
        print("\n" + "-" * 50 + "\n")

    # 2. 使用不同模型
    prompt2 = "解释量子计算的基本原理。"
    result2 = get_completion(prompt2, model_name="deepseek-r1:8b")

    if result2:
        print("使用不同模型的生成结果:")
        print(result2)

    # 3. 处理较长的回复
    print("\n生成更长的回复:")
    long_prompt = "详细解释气候变化的原因和影响。"
    long_result = get_completion(long_prompt, model_name="deepseek-r1:8b")

    if long_result:
        print(long_result)

