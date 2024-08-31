import torch
import torch.optim as optim

from pytorch_lightning import LightningModule

from lctgen.core.registry import registry

from extended.refiner.base_refiner import BaseRefiner

class LCTGenExtended(LightningModule):
    def __init__(self, config):
        super().__init__()

        self.config = config
        self.refiner = BaseRefiner(config)

        model_cls = registry.get_model(self.config.MODEL.TYPE)
        self.lctgen = model_cls.load_from_checkpoint("./checkpoints/example.ckpt", config=self.config, metrics={}, strict=False)
        self.lctgen.eval()

        self.lr = self.config.TRAIN.LR

    def configure_optimizers(self):
        return optim.AdamW(self.refiner.parameters(), lr=self.lr, betas=(0.9, 0.999), weight_decay=self.config.TRAIN.WEIGHT_DECAY, amsgrad=True, eps=1e-09)

    def forward(self, batch, mode):
        batch["text"] = self.refiner(batch, mode)
        result = self.lctgen(batch, mode)
        return 

    def training_step(self, batch, batch_idx):
        output = self.forward(batch, 'train')
        return output

    def validation_step(self, batch, batch_idx):
        output = self.forward(batch, 'val')
        return output

    def test_step(self, batch, batch_idx):
        output = self.forward(batch, 'test')
        return output
