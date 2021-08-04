import pickle
import socket
import json
import time
from PIL import Image

import numpy as np
import cv2
import matplotlib.pyplot as plt

from api import load_all, predict_on_image


HOST = "127.0.0.1"
PORT = 31415
START_MSG = "{START}"
END_MSG = "{END}"


def get_image(full_message):
    full_message = full_message[len(START_MSG) : -len(END_MSG)]
    list_image = json.loads(full_message)
    image = np.array(list_image, dtype=np.uint8)
    return image


modules = load_all()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Waiting for client to connect")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {(conn, addr)}")
        full_msg: str = ""
        new_msg = True
        while True:
            data = conn.recv(4096)
            if new_msg:
                new_msg = False
                print("New Message!")
            full_msg += data.decode("utf-8")
            if full_msg[-len(END_MSG) :] == END_MSG:
                new_msg = True
                print("Message Revd")
                img_recv = get_image(full_msg)
                vertices = predict_on_image(img_recv, modules)
                if len(vertices) > 0:
                    message_to_send_str = (
                        START_MSG
                        + json.dumps(vertices[0].tolist(), separators=(",", ":"))
                        + END_MSG
                    )
                else:
                    message_to_send_str = (
                        START_MSG + json.dumps([], separators=(",", ":")) + END_MSG
                    )
                conn.send(bytes(message_to_send_str, "utf-8"))
                print("Sent message")
                full_msg = ""
