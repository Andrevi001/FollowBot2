from ultralytics import YOLO

class TargetDetector: 

    class Punto:
        def __init__(self, x, y, visibility):
            self.x = x
            self.y = y
            self.visibility = visibility

    def __init__(self, filePath):
        self.detector = YOLO(filePath)

    def detect(self, frame):
        targets = []

        raw_targets = self.detector(frame, imgsz=(256, 320), verbose=False)

        if raw_targets[0].keypoints is None or len(raw_targets[0].keypoints) == 0:
            return targets
        
        for landmarks, scores in zip(raw_targets[0].keypoints.xyn, raw_targets[0].keypoints.conf):
            landmarks = landmarks.numpy()
            scores = scores.numpy()
            pose = []
            for kps, conf in zip(landmarks, scores):
                pose.append(self.Punto(kps[0], kps[1], conf))

            targets.append(pose)
            

        return targets
