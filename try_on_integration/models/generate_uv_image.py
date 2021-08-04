import numpy as np
import cv2

with open(
        "/home/arush/Desktop/3dFaceConstructionPythonPytorch/FR3D_custom/production/server_side_code/models/UV_reduced.npy",
        "rb") as f:
    UV = np.load(f)

RES = 4096
image = np.zeros((RES, RES, 3))

for i in range(len(UV)):
    to_draw = (int(UV[i][0] * RES), int(UV[i][1] * RES))
    image = cv2.circle(image, to_draw, 1, (255, 255, 255), -1)
    image = cv2.putText(image, "P:" + str(i), to_draw,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 255, 255), 1,
                        cv2.LINE_AA)

cv2.imwrite(
    "/home/arush/Desktop/3dFaceConstructionPythonPytorch/FR3D_custom//production/server_side_code/models/uv_image_helper_reduced.png",
    cv2.flip(image, 0))
