import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

while True:
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()
    cv2.imshow("image1",frame1)
    cv2.imshow("image2",frame2)
    cv2.waitKey(3)
    ret,frame = cap2.read()
    if ret == True:
        frame = cv2.flip(frame,2)
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(2) == ord('q'):
            break
    else:
        break
cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()

