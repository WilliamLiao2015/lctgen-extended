from configs.paths import prompts_dir
from imports.system import os
from imports.packages import requests


def inference_llama3_llm(query, stream=False):
    with open(f"{prompts_dir}/sys_non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        system_prompt = fp.read()

    with open(f"{prompts_dir}/non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        user_prompt = fp.read()

    user_prompt = user_prompt.replace("INSERT_QUERY_HERE", query)
    response = requests.post("https://api.together.xyz/v1/chat/completions", headers={
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
        "Content-Type": "application/json"
    }, json={
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "messages": [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_prompt }
        ],
        "temperature":0.75,
        "top_p":0.9,
        "max_tokens": 1024,
        "stream_tokens": stream
    })

    llm_result = response.json()["choices"][0]["message"]["content"]

    return llm_result
