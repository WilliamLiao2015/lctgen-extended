from configs.paths import prompts_dir
from imports.packages import requests


def inference_llama3_llm(query):
    with open(f"{prompts_dir}/sys_non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        system_prompt = fp.read()

    with open(f"{prompts_dir}/non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        user_prompt = fp.read()

    user_prompt = user_prompt.replace("INSERT_QUERY_HERE", query)

    response = requests.post("http://localhost:1234/v1/chat/completions", json={
        "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        "messages": [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_prompt }
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    })

    llm_result = response.json()["choices"][0]["message"]["content"]

    return llm_result
