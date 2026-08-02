import cv2
import config


class FaceDetector: 
    def __init__(self):
        self.detector = cv2.FaceDetectorYN.create("Modelli/yunet.onnx", "", (config.width, config.height))
        self.detector.setInputSize((config.width, config.height))


    def detect(self, frame):
        _, faces = self.detector.detect(frame)
        return faces
