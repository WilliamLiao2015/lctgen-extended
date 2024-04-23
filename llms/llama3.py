from configs.paths import prompts_dir
from imports.system import json
from imports.packages import requests


def inference_llama3_llm(query, stream=False):
    with open(f"{prompts_dir}/sys_non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        system_prompt = fp.read()

    with open(f"{prompts_dir}/non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        user_prompt = fp.read()

    user_prompt = user_prompt.replace("INSERT_QUERY_HERE", query)
    response = requests.post("https://fumes-api.onrender.com/llama3", json={
        "prompt": json.dumps({
            "systemPrompt": system_prompt, 
            "user": user_prompt
        }),
        "temperature":0.75,
        "topP":0.9,
        "maxTokens": 1024
    }, stream=stream)

    llm_result = ""

    if stream:
        for chunk in response.iter_content(chunk_size=1024):  
            if chunk:
                llm_result += chunk.decode("utf-8")
    else:
        llm_result = response.text

    return llm_result
