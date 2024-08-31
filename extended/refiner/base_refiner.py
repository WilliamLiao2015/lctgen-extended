import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import torch

from lctgen.models.blocks import MLP, pos2posemb
from lctgen.models.detr_model import DETRAgentQuery

class BaseRefiner(DETRAgentQuery):
    def __init__(self, cfg):
        super().__init__(cfg)

        AGENT_ATTR_DIM = 8 # LCTGen uses 8 dims for agent attributes
        self.agent_decode = MLP([
            self.model_cfg.hidden_dim * 2, # DETRAgentQuery used: 256 * 2 = 512
            self.model_cfg.hidden_dim,
            AGENT_ATTR_DIM
        ])

    def forward(self, batch, mode):
        attr_cfg = self.model_cfg.ATTR_QUERY
        pos_enc_dim = attr_cfg.POS_ENCODING_DIM # 256

        # Map Encoder
        b = batch['lane_inp'].shape[0]
        device = batch['lane_inp'].device
        line_enc = self._map_lane_encode(batch['lane_inp'].float())
        empty_context = torch.ones([b, line_enc.shape[-1]]).to(device)
        line_enc, _ = self._map_feature_extract(line_enc, batch['lane_mask'], empty_context)
        line_enc = line_enc[:, :batch['center_mask'].shape[1]]

        attr_query_input = batch['text']
        attr_dim = attr_query_input.shape[-1]
        attr_query_encoding = pos2posemb(attr_query_input, pos_enc_dim//attr_dim) # 256 // 8 = 32

        attr_query_encoding = self.query_embedding_layer(attr_query_encoding)
        learnable_query_embedding = self.actor_query.repeat(b, 1, 1)
        query_encoding = learnable_query_embedding + attr_query_encoding

        # Agent Attribute Decoder
        result = self.agent_decode(query_encoding)

        return result
