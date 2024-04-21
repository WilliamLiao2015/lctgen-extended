from imports import in_colab


if in_colab: base_dir = "/content"
else: base_dir = "."


lctgen_dir = f"{base_dir}/lctgen"
prompts_dir = f"{lctgen_dir}/lctgen/gpt/prompts/attr_ind_motion"
