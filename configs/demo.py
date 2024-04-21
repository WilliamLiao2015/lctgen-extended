from configs.paths import lctgen_dir
from imports.lctgen import get_config, registry, load_all_map_vectors


cfg_file = f"{lctgen_dir}/cfgs/demo_inference.yaml"
cfg = get_config(cfg_file)

model_cls = registry.get_model(cfg.MODEL.TYPE)
model = model_cls.load_from_checkpoint(cfg.LOAD_CHECKPOINT_PATH, config=cfg, metrics=[], strict=False)
model.eval()

map_data_file = f"{lctgen_dir}/data/demo/waymo/demo_map_vec.npy"
map_vecs, map_ids = load_all_map_vectors(map_data_file)
