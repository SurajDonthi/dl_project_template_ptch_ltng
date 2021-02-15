import os
from argparse import ArgumentParser

from pathlib2 import Path
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from pytorch_lightning.loggers.test_tube import TestTubeLogger

from src.data import CustomDataLoader
from src.engine import Engine
from src.utils import save_args


def main():
    tt_logger = TestTubeLogger(save_dir=args.log_path, name="",
                               description=args.description, debug=False,
                               create_git_tag=args.git_tag)
    tt_logger.experiment

    log_dir = Path(tt_logger.save_dir) / f"version_{tt_logger.version}"

    checkpoint_dir = log_dir / "checkpoints"
    os.makedirs(checkpoint_dir, exist_ok=True)
    chkpt_callback = ModelCheckpoint(checkpoint_dir,
                                     #  monitor='Loss/val_loss',
                                     #  save_last=True,
                                     #  mode='min',
                                     #  save_top_k=1
                                     )

    data_loader = CustomDataLoader.from_argparse_args(args,

                                                      )

    model = Engine(None)

    save_args(args, log_dir)

    trainer = Trainer.from_argparse_args(args, logger=tt_logger,
                                         checkpoint_callback=chkpt_callback,
                                         #   early_stop_callback=False,
                                         #   weights_summary='full',
                                         #   gpus=1,
                                         #   max_epochs=20
                                         )

    trainer.fit(model, data_loader)
    # trainer.test(model)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-gt', '--git_tag', type=bool,
                        default=False, help='Creates a git tag if true')
    parser = CustomDataLoader.add_argparse_args()
    parser = Engine.add_model_specific_args(parser)
    parser = Trainer.add_argparse_args(parser)
    args = parser.parse_args()

    main(args)
