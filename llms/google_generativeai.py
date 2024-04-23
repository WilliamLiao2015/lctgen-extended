from configs.paths import prompts_dir
from imports.packages import genai


def get_google_llm(model_name="gemini-1.0-pro-latest", generation_config=None, safety_settings=None):
    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048
    } if generation_config is None else generation_config

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ] if safety_settings is None else safety_settings

    llm_model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config, safety_settings=safety_settings)

    return llm_model


def inference_google_llm(llm_model, query):
    prompt = "## INSTRUCTIONS\n"

    with open(f"{prompts_dir}/sys_non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        prompt += fp.read()
    prompt += "\n---\n## QUERIES\n"
    with open(f"{prompts_dir}/non_api_cot_attr_20m.prompt", "r", encoding="utf-8") as fp:
        prompt += fp.read()

    prompt = prompt.replace("INSERT_QUERY_HERE", query)
    result = llm_model.generate_content(prompt)
    llm_result = result.text

    return llm_result
