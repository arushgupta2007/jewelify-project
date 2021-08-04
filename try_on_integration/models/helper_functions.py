#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import scipy.io as scio
import numpy as np

parent_dir = "/home/arush/Desktop/3dFaceConstructionPythonPytorch/FR3D_custom/production/server_side_code/models/"
point_to_search = int(input())


def load_triangulation_map():
    return np.load(f"{parent_dir}/tri_reduced.npy", allow_pickle=True)


def load_uv_map():
    # return scio.loadmat(os.path.join(parent_dir, "BFM_UV.mat"))["UV"]
    with open(
            f"{parent_dir}/uv_reduced.npy",
            "rb") as f:
        UV = np.load(f)
    return UV


tri = load_triangulation_map().T
uv = load_uv_map()

print(tri)
print(uv)

for i in range(len(tri[0])):
    for j in range(len(tri)):
        if tri[j][i] == point_to_search:
            print(tri[0][i], tri[1][i], tri[2][i], i)

print()
print(uv[point_to_search])
