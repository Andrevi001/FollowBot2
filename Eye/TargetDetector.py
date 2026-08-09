from rtmlib import Body
import numpy as np
import config

class TargetDetector: 

    class Punto:
        def __init__(self, x, y, visibility):
            self.x = x
            self.y = y
            self.visibility = visibility

    def __init__(self, filePath=None):
        self.detector = Body(
            mode='lightweight', 
            backend='onnxruntime', 
            device='cpu'
        )

    def detect(self, frame):
        targets = []

        raw_keypoints, scores = self.detector(frame)

        if len(raw_keypoints) == 0:
            return targets
        
        raw_keypoints = raw_keypoints / np.array([config.width, config.height])
        for landmarks, p_scores in zip(raw_keypoints, scores):
            pose = []
            for (x, y), conf in zip(landmarks, p_scores):
                pose.append(self.Punto(x, y, conf))

            targets.append(pose)
            

        return targets
