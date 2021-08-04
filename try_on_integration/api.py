"""
    Helper functions for main.py

    This file contains helper function for the main script.
    Helper functions include:

    - predict_on_image(img)
"""


import time

import numpy as np
import cv2
import torch
import torchvision.transforms as transforms

from models import load_model, load_face_detector, load_triangulation_map, load_uv_map
from utils.ddfa import ToTensorGjz, NormalizeGjz
from utils.inference import (
    parse_roi_box_from_landmark,
    crop_img,
    predict_dense,
    # predict_68pts,
)


STD_SIZE = 120


def load_all():
    """
    Load the required modules:
    ML model, face regressor, face detector, triangulation map, uv map, transform object
    """
    model = load_model(mode="cpu")
    model.eval()
    face_regressor, face_detector = load_face_detector()
    return {
        "model": model,
        "face_regressor": face_regressor,
        "face_detector": face_detector,
        "triangulation_map": load_triangulation_map(),
        "uv_map": load_uv_map().flatten(),
        "transform": transforms.Compose(
            [ToTensorGjz(), NormalizeGjz(mean=127.5, std=128)]
        ),
    }


def predict_on_image(img: np.ndarray, loaded_modules: dict):
    """
    Predict the facial landmarks of the person in the given image.

    Parameters
    ----------
    img : np.ndarray
        The 640x480 image of the person
    loaded_modules : dict
        A dictionary containing all loaded modules (ml model, face_regressor, face_detector, triangulation_map, uv_map, transform)

    Returns
    -------
    The facial landmark coordinates.
    """

    # check amount of time taken for this process (debugging only)
    start_time = time.time()

    # list of all found faces
    faces = []

    # list of coordinates of facial landmarks
    vertices_list = []

    # get all faces
    rects = loaded_modules["face_detector"](img, 1)
    for rect in rects:
        pts_raw = loaded_modules["face_regressor"](img, rect).parts()
        pts = np.array([[pt.x, pt.y] for pt in pts_raw]).T
        faces.append(pts)

    # if no faces found just leave
    if len(faces) == 0:
        return []

    # use only first face in the faces list

    # crop import region (the face)
    roi_box = parse_roi_box_from_landmark(faces[0])
    roi_img = crop_img(img, roi_box)

    # if the face has not rows, just leave (has happened for some reason, this is to avoid that issue)
    if len(roi_img) == 0:
        return []

    # resize image to required size
    roi_img = cv2.resize(
        roi_img, dsize=(STD_SIZE, STD_SIZE), interpolation=cv2.INTER_LINEAR
    )

    # pre-process image before feeding it to the model
    input_to_model = loaded_modules["transform"](roi_img).unsqueeze(0)

    # evaluate the image
    with torch.no_grad():
        # pass input to model, and convert to right shape and size
        param = (
            loaded_modules["model"](
                input_to_model
            )  # this is where the input is fed to the model
            .squeeze()
            .cpu()
            .numpy()
            .flatten()
            .astype(np.float32)
        )
        # pts68 = predict_68pts(param, roi_box)

        # get dense network of all landmarks
        dense = predict_dense(param, roi_box)
        vertices_list.append(dense)

    # get time taken (debugging only)
    time_taken = time.time() - start_time

    # return output
    return vertices_list
