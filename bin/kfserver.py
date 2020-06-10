"""Script to serve model prediction"""
import os
from http import HTTPStatus
from typing import Dict, List

import joblib
import numpy as np
import tornado

from utils import utils

import kfserving

MODEL_NAME = os.environ.get("MODEL_NAME", "randomforest")
# TODO: load from s3
MODEL_ARTIFACT = os.environ.get("MODEL_ARTIFACT", f"outputs/{MODEL_NAME}.pkl")


class ModelService(kfserving.KFModel):
    """Class to serve model predictions."""
    def __init__(self, name: str, model_artifact: str):
        super().__init__(name)
        self.name = name
        self.model_artifact = model_artifact

    def load(self):
        """load training artifacts"""
        self.model = utils.load_model(self.model_artifact)
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        """Conduct inference"""
        assert request["instances"] is not None
        try:
            instances = request["instances"]
            inputs = np.array(instances)
        except KeyError:
            return tornado.web.HTTPError(
                status_code=HTTPStatus.BAD_REQUEST,
                reason=(
                    f"The request format is invalid, check your request object."
                ))
        try:
            result = self.model.predict(inputs).tolist()
            return {"predictions": result}
        except Exception as e:
            raise Exception(f"Failed to predict with {e}")


def serve():
    model_service = ModelService(
        name=MODEL_NAME,
        model_artifact=MODEL_ARTIFACT,
    )
    model_service.load()
    kfserver = kfserving.KFServer()
    kfserver.start(models=[model_service])


if __name__ == "__main__":
    serve()
