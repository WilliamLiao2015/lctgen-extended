from scripts.colab import in_colab


if in_colab: base_dir = "/content"
else: base_dir = "."


lctgen_extended_dir = f"{base_dir}/lctgen-extended"
lctgen_dir = f"{base_dir}/lctgen"
prompts_dir = f"{lctgen_dir}/gpt/prompts/attr_ind_motion"
