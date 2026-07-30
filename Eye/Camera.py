import picamera2
import cv2
import config

class Camera():

    def __init__(self):
        self.picam2 = picamera2.Picamera2()

    def begin(self):
        conf = self.picam2.create_preview_configuration(main={"size": (config.width, config.height)})
        self.picam2.configure(conf)
        self.picam2.start()

    def captureFrame(self):
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        return frame

    def close(self):
        self.picam2.close()