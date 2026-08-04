import cv2
import time
from config import RTSP_URL
cap = cv2.VideoCapture(RTSP_URL)
if not cap.isOpened():
    print("Error:Could not open video stream.")
    raise SystemExit(1)
ok,frame = cap.read()
if not ok:
    print("Error: Could not read frame from video stream.")
    raise SystemExit(1)
start = time.time()
Success_num = 0
fail_num = 0
while time.time()-start<60:
    ok,frame = cap.read()
    if ok:
        Success_num += 1
    else:
        fail_num += 1
elapsed_time = time.time()-start
print("success_fps:",Success_num/elapsed_time)
print("fail_fps",fail_num/elapsed_time)
print("total_fps",(Success_num + fail_num)/elapsed_time)
cap.release