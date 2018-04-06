import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

kernel = np.ones((5, 5), np.uint8)
background = None

writer = None
count = 0

while True:
    _, frame = cap.read()

    if writer:
        writer.write(frame)
        count -= 1
        if count <= 0:
            writer = None
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (49, 49), 0)

    if background is None:
        background = gray
        continue

    diff = cv2.absdiff(background, gray)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)

    sth = False
    # 显示矩形框
    image, contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) > 1500:
            sth = True
            break
        # if cv2.contourArea(c) < 1500:
        #     continue
        # (x, y, w, h) = cv2.boundingRect(c)
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # cv2.imshow('contours', frame)
    # cv2.imshow('dis', diff)

    if sth:
        writer = cv2.VideoWriter(
                    "{}.avi".format(time.strftime("%Y%m%d-%H%M%S")), 
                    cv2.VideoWriter_fourcc('M','P','4','2'), 
                    15, 
                    size
                )
        count = 60
        background = None
        continue

    time.sleep(0.06)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    background = gray

cap.release()
cv2.destroyAllWindows()
