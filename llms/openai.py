from imports.lctgen import get_config, registry
from configs.paths import prompts_dir


def get_openai_llm(llm_model_name="gpt-3.5-turbo"):
    llm_cfg = get_config(f"{prompts_dir}/non_api_cot_attr_20m.yaml")
    llm_cfg.merge_from_list(["LLM.CODEX.MODEL", llm_model_name])

    llm_model = registry.get_llm("codex")(llm_cfg)

    return llm_model


def inference_openai_llm(llm_model, query):
    llm_result = llm_model.forward(query)

    return llm_result
