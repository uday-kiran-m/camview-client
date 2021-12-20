import cv2

vid = cv2.VideoCapture('rtsp://viewuser:viewuser123@192.168.1.15:554/Streaming/Channels/101')
vid.set(cv2.CAP_PROP_FPS,15)
        # print('cap')
i = 0
while Exception != KeyboardInterrupt :#change to a variable
    ret ,frame = vid.read()
    print(ret)
else:
    vid.release()
