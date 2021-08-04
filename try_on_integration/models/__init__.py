"""
Helper function to load files
This file contains some useful helper functions to load files
"""

# imports
import os
import numpy as np
import scipy.io as scio
import dlib
import torch

# if os.environ.get("JEWELIFY_PROD") is None:
#     from production.server_side_code.utils import mobilenet_v1
# else:
#     from utils import mobilenet_v1
from utils import mobilenet_v1


# define parent dir
parent_dir = os.path.dirname(os.path.abspath(__file__))


def load_uv_map() -> np.ndarray:
    """
    Load uv map from ./uv_reduced.npy

    Returns
    -------
    UV: np.ndarray -> The numpy array containing the uv map with size (10000, 2)
    """
    with open(f"{parent_dir}/uv_reduced.npy", "rb") as f:
        UV: np.ndarray = np.load(f)
    return UV


def load_triangulation_map() -> np.ndarray:
    """
    Load triangulation data from ./tri_reduced.npy

    Returns
    -------
    np.ndarray -> The numpy array containing the triangulation data,
                    size: (19979, 3)
    """
    return np.load(f"{parent_dir}/tri_reduced.npy")


def load_face_detector():
    """
    Load dlib face face detector and face regressor from ./shape_predictor_68...

    Returns
    -------
    face_regressor: Any -> the face regressor
    face_detector: Any -> the face detector
    """
    dlib_landmark_model = os.path.join(
        parent_dir, "shape_predictor_68_face_landmarks.dat"
    )
    face_regressor = dlib.shape_predictor(dlib_landmark_model)
    face_detector = dlib.get_frontal_face_detector()
    return face_regressor, face_detector


def load_model(mode="cpu"):
    """
    Load ML model from ./phase1_wpdc_vdc.pth.tar

    Returns
    -------
    model: mobilenet_v1.MobileNet -> The pytorch model
    """

    checkpoint_fp = os.path.join(parent_dir, "phase1_wpdc_vdc.pth.tar")
    arch = "mobilenet_1"
    checkpoint = torch.load(checkpoint_fp, map_location=lambda storage, loc: storage)[
        "state_dict"
    ]
    model = getattr(mobilenet_v1, arch)(
        num_classes=62
    )  # 62 = 12(pose) + 40(shape) +10(expression)
    model_dict = model.state_dict()
    # because the model is trained by multiple gpus, prefix module should be removed
    for k in checkpoint.keys():
        model_dict[k.replace("module.", "")] = checkpoint[k]
    model.load_state_dict(model_dict)
    if mode == "gpu":
        model = model.cuda()
    return model
