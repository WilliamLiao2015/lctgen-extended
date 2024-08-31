import json

import torch

from torch.utils.data import Dataset

from lctgen.inference.utils import output_formating_cot, map_retrival, get_map_data_batch, load_all_map_vectors

map_data_file = f"../data/demo/demo_map_vec.npy"
map_vecs, map_ids = load_all_map_vectors(map_data_file)

class StructureRepresentationDataset(Dataset):
    def __init__(self, path: str, cfg):
        self.path = path
        self.cfg = cfg
        with open(path, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        MAX_AGENT_NUM = 32

        try:
            # Use the agent_vector and map_vector from the dataset if available
            agent_vector = self.data[idx]["actor_vectors"]
            map_vector = self.data[idx]["map_vector"]
        except KeyError:
            # Format LLM output to Structured Representation (agent and map vectors)
            agent_vector, map_vector = output_formating_cot(self.data[idx]["llm_result"])
            agent_num = len(agent_vector)
            vector_dim = len(agent_vector[0])
            agent_vector = agent_vector + [[-1]*vector_dim] * (MAX_AGENT_NUM - agent_num)

        agent_num = len(agent_vector)
        vector_dim = len(agent_vector[0])

        # retrive map from map dataset
        sorted_idx = map_retrival(map_vector, map_vecs)[:1]
        map_id = map_ids[sorted_idx[0]]

        # load map data
        data = get_map_data_batch(map_id, self.cfg)

        # inference with LLM-output Structured Representation
        data["text"] = torch.tensor(agent_vector, dtype=data["text"].dtype)[None, ...]
        data["agent_mask"] = torch.tensor([1]*agent_num + [0]*(MAX_AGENT_NUM - agent_num), dtype=data["agent_mask"].dtype)[None, ...]

        return data
