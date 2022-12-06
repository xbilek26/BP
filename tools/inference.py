import os
import logging
import warnings
import cv2
import numpy as np

from pytorch_lightning import Trainer, seed_everything
from torch.utils.data import DataLoader

from anomalib.config import get_configurable_parameters
from anomalib.data.inference import InferenceDataset
from anomalib.data import get_datamodule
from anomalib.models import get_model
from anomalib.utils.callbacks import LoadModelCallback, get_callbacks
from anomalib.utils.loggers import configure_logger, get_experiment_logger
from anomalib.pre_processing.transforms import Denormalize

logger = logging.getLogger("anomalib")

logging.disable(logging.CRITICAL) # disable printing logs to console
warnings.filterwarnings("ignore") # disable printing warnings to console

def retrain():

    model = 'padim'
    my_config = 'tools/config/padim.yaml' #no validation
    pretrained_weights = 'pretrained-models/padim/model.ckpt'
    log_level = 'INFO'

    configure_logger(level=log_level)

    if log_level == "ERROR":
        warnings.filterwarnings("ignore")

    config = get_configurable_parameters(model_name=model, config_path=my_config)

    if config.project.seed:
        seed_everything(config.project.seed)

    datamodule = get_datamodule(config)
    model = get_model(config)
    experiment_logger = get_experiment_logger(config)
    callbacks = get_callbacks(config)

    trainer = Trainer(**config.trainer, logger=experiment_logger, callbacks=callbacks)
    logger.info("Training the model.")
    trainer.fit(model=model, datamodule=datamodule, ckpt_path=pretrained_weights) # use pretrained model

    logger.info("Loading the best model weights.")
    load_model_callback = LoadModelCallback(weights_path=trainer.checkpoint_callback.best_model_path)
    trainer.callbacks.insert(0, load_model_callback)

    #logger.info("Testing the model.")                  --NO TESTING
    #trainer.test(model=model, datamodule=datamodule)   --NO TESTING

def infer():

    my_config = 'tools/config/padim.yaml'
    weights = 'temp/padim/test_app/weights/model.ckpt'
    input = 'temp/frames'
    output = 'temp/output'

    config = get_configurable_parameters(config_path=my_config)

    model = get_model(config)
    callbacks = get_callbacks(config)

    trainer = Trainer(**config.trainer, callbacks=callbacks)

    transform_config = config.dataset.transform_config.val if "transform_config" in config.dataset.keys() else None
    dataset = InferenceDataset(
        path=input, image_size=tuple(config.dataset.image_size), transform_config=transform_config
    )
    dataloader = DataLoader(dataset)
    #predictions = trainer.predict(model=model, dataloaders=[dataloader])

    #predictions = trainer.predict(model=model, dataloaders=[dataloader], ckpt_path=weights)

    #for frame in trainer.predict(model=model, dataloaders=[dataloader], ckpt_path=weights):
    #    pred_score = frame["pred_scores"][0]
    #    pred_labels = frame["pred_labels"][0]
    #    print("Frame", frame["image_path"][0], pred_score, pred_labels)

    return trainer.predict(model=model, dataloaders=[dataloader], ckpt_path=weights)