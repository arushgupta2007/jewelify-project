import cv2

from api import load_all, predict_on_image

modules = load_all()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(rgb_image.shape)
    vert = predict_on_image(rgb_image, modules)
    if len(vert) != 0:
        vertices = vert[0]
        for i in range(vertices.shape[1]):
            point = (int(vertices[0, i]), int(vertices[1, i]))
            frame = cv2.circle(frame, point, 1, (255, 255, 255), -1)
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
