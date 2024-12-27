from flask_restx import Namespace, Model
from typing import Dict

from .mongo import *

MODEL_NAME = "model_name"
MODEL_DEFINITION = "model_definition"
MODEL_ERROR = "Model details must be a dict with the keys model_name: str and model_definition: Dict "


def get_restx_model(namespace: Namespace, model_details: Dict[str, Dict]) -> Model:
    """This function will register the give model with the namespace and return the given flask_restx model name"""
    if not (MODEL_NAME in model_details and MODEL_DEFINITION in model_details):
        raise ValueError("Invalid Model Details! %s" % MODEL_ERROR)
    return namespace.model(model_details.get(MODEL_NAME), model_details.get(MODEL_DEFINITION))
