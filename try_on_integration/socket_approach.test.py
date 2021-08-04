import socket
import json
import time
import cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 31415
START_MSG = "{START}"
END_MSG = "{END}"


def get_vertices(full_msg):
    full_msg = full_msg[len(START_MSG) : -len(END_MSG)]
    vertices = json.loads(full_msg)
    return np.array(vertices)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        json_data = json.dumps(rgb_image.tolist(), separators=(",", ":"))
        msg = START_MSG + json_data + END_MSG
        s.send(bytes(msg, "utf-8"))
        print("Sent Message")
        recv_full_msg = ""
        new_msg = True
        while True:
            data = s.recv(4096)
            if new_msg:
                new_msg = False
                print("New Message!")
            recv_full_msg += data.decode("utf-8")
            if recv_full_msg[-len(END_MSG) :] == END_MSG:
                break

        print("Recvd message")

        vertices = get_vertices(recv_full_msg)
        if len(vertices) != 0:
            for i in range(vertices.shape[1]):
                point = (int(vertices[0, i]), int(vertices[1, i]))
                frame = cv2.circle(frame, point, 1, (255, 255, 255), -1)

        cv2.imshow("Window", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
