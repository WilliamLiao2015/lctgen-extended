import argparse
import pathlib
import random
import sys
import os

from datetime import datetime

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

import logging

logging.captureWarnings(True)
logging.getLogger('py.warnings').setLevel(logging.ERROR)

import numpy as np
import torch

from torch.utils.data import DataLoader
from pytorch_lightning import Trainer as BaseTrainer, seed_everything
from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger

from lctgen.config.default import get_config

from trafficgen.utils.typedef import *

from model import LCTGenExtended
from dataset import StructureRepresentationDataset

def current_time_str():
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    return date_time

class Trainer(BaseTrainer):
    def __init__(self, config):
        self.config = config
        self.profier = 'simple'
        avalible_gpus = [i for i in range(torch.cuda.device_count())]

        seed_everything(self.config.SEED, workers=True)

        lr_monitor = LearningRateMonitor(logging_interval='step')
        callbacks = [lr_monitor]

        if self.config.SAVE_CHECKPOINT:
            checkpoint_callback = ModelCheckpoint(
                monitor="val/full_loss",
                mode="min",
                auto_insert_metric_name=True,
                save_last=True,
                save_top_k=1
            )
            callbacks.append(checkpoint_callback)
            enable_checkpointing = True
        else:
            enable_checkpointing = False

        # use all avalible GPUs
        if self.config.GPU is None or len(self.config.GPU) > torch.cuda.device_count():
            self.config['GPU'] = avalible_gpus

        # device config
        device_cfg = {}
        if len(self.config.GPU) > 1:
            device_cfg['strategy'] = 'ddp'
            device_cfg['devices'] = self.config.GPU
            device_cfg['accelerator'] = 'gpu'
        elif len(self.config.GPU) == 1:
            device_cfg['devices'] ='auto'
            device_cfg['accelerator'] ='gpu'
        else:
            device_cfg['devices'] ='auto'
            device_cfg['accelerator'] ='cpu'
        self.device_cfg = device_cfg

        print('GPU: ', self.config.GPU)

        self._config_save_dir()
        self._config_logger()
        self._config_data()

        super().__init__(max_epochs=self.config.MAX_EPOCHES,
            log_every_n_steps=self.config.LOG_INTERVAL_STEPS,
            check_val_every_n_epoch=self.config.VAL_INTERVAL,
            limit_val_batches = self.config.LIMIT_VAL_BATCHES,
            default_root_dir=self.save_dir,
            logger=self.logger,
            callbacks=callbacks,
            profiler=self.profier,
            enable_checkpointing=enable_checkpointing,
            **self.device_cfg,
            gpus=0
        )

        self.extended_model = LCTGenExtended(config)

    def _config_logger(self):
        exp_name = current_time_str()
        self.logger = TensorBoardLogger(self.save_dir, name=exp_name)

    def _config_data(self):
        self.data_loaders = {}
        
        for split in ['train', 'val', 'test']:
            key = split.upper()
            dataset = StructureRepresentationDataset(self.config[key].DATASET_PATH, self.config)
            batch_size = self.config[key].BATCH_SIZE

            self.data_loaders[split] = DataLoader(
                dataset,
                batch_size=batch_size,
                shuffle=self.config[key].SHUFFLE,
                num_workers=self.config[key].NUM_WORKERS
            )

    def _config_save_dir(self):
        if self.config.EXPERIMENT_NAME:
            self.exp_name = self.config.EXPERIMENT_NAME
        else:
            self.exp_name = current_time_str()

        # create save dirs
        if self.config.SAVE_DIR:
            self.save_dir = os.path.join(self.config.SAVE_DIR , self.config.EXPERIMENT_DIR, str(self.exp_name))
        else:
            self.save_dir = os.path.join(self.config.ROOT_DIR, self.config.EXPERIMENT_DIR, str(self.exp_name))

        pathlib.Path(self.save_dir).mkdir(parents=True, exist_ok=True)

        print(self.save_dir)

        # save config file
        config_dir = os.path.join(self.save_dir, 'config.yaml')
        with open(config_dir, 'w') as file:
            self.config.dump(stream=file)

    def train(self):
        if self.config.LOAD_CHECKPOINT_TRAINER and self.config.LOAD_CHECKPOINT_PATH is not None:
            ckpt_path = self.config.LOAD_CHECKPOINT_PATH
            print('loading training state from checkpoint: {}'.format(ckpt_path))
        else:
            ckpt_path = None
        self.fit(self.extended_model, self.data_loaders['train'], self.data_loaders['val'], ckpt_path=ckpt_path)

        try:
            ckpt_path = self.checkpoint_callback.best_model_path
            print('perform evaluation with best checkpoint on a single GPU')
            self.test(self.extended_model, self.data_loaders['test'], ckpt_path=ckpt_path)
        except Exception as e:
            print('test best model failed: {}'.format(e))
            print('test last model instead')
            self.test(self.extended_model, self.data_loaders['test'])

    def eval(self):
        if self.config.LOAD_CHECKPOINT_TRAINER and self.config.LOAD_CHECKPOINT_PATH is not None:
            ckpt_path = self.config.LOAD_CHECKPOINT_PATH
            print('loading training state from checkpoint: {}'.format(ckpt_path))
        else:
            ckpt_path = None
        self.test(model=self.extended_model, dataloaders=self.data_loaders['test'], ckpt_path=ckpt_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-type",
        choices=["train", "eval"],
        required=True,
        help="run type of the experiment (train or eval)",
    )
    parser.add_argument(
        "--exp-config",
        type=str,
        required=True,
        help="path to config yaml containing info about experiment",
    )
    parser.add_argument(
        "opts",
        default=None,
        nargs=argparse.REMAINDER,
        help="Modify config options from command line",
    )

    args = parser.parse_args()
    config = get_config(args.exp_config, args.opts)

    random.seed(config.SEED)
    np.random.seed(config.SEED)
    torch.manual_seed(config.SEED)

    trainer = Trainer(config)

    if args.run_type == "train":
        trainer.train()
    elif args.run_type == "eval":
        trainer.eval()
