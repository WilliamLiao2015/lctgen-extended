from setup import in_colab


if in_colab: base_dir = "/content"
else: base_dir = "."


prompts_dir = f"{base_dir}/lctgen/lctgen/gpt/prompts/attr_ind_motion"
