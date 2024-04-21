from imports.packages import torch, np
from imports.lctgen import output_formating_cot, map_retrival, get_map_data_batch, transform_traj_output_to_waymo_agent
from imports.trafficgen import *


def inference(model, cfg, map_vecs, map_ids, llm_result):
    # Format LLM output to Structured Representation (agent and map vectors)
    MIN_LENGTH = 4.0
    MIN_WIDTH = 1.5

    MAX_TIMESTEPS = 50
    MAX_AGENT_NUM = 32

    agent_vector, map_vector = output_formating_cot(llm_result)

    agent_num = len(agent_vector)
    vector_dim = len(agent_vector[0])
    agent_vector = agent_vector + [[-1]*vector_dim] * (MAX_AGENT_NUM - agent_num)

    # retrive map from map dataset
    sorted_idx = map_retrival(map_vector, map_vecs)[:1]
    map_id = map_ids[sorted_idx[0]]

    # load map data
    data = get_map_data_batch(map_id, cfg)

    # inference with LLM-output Structured Representation
    data['text'] = torch.tensor(agent_vector, dtype=data['text'].dtype)[None, ...]
    data['agent_mask'] = torch.tensor([1]*agent_num + [0]*(MAX_AGENT_NUM - agent_num), dtype=data['agent_mask'].dtype)[None, ...]

    model_output = model.forward(data, 'val')['text_decode_output']
    output_scene = model.process(model_output, data, num_limit=1, with_attribute=True, pred_ego=True, pred_motion=True)

    agents = transform_traj_output_to_waymo_agent(output_scene[0])

    for t in range(MAX_TIMESTEPS):
        for agent in agents[t]:
            agent.length_width = np.clip(agent.length_width, [MIN_LENGTH, MIN_WIDTH], [10.0, 5.0])

    return data, agents
