import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class TargetDetector: 
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path='Modelli/pose_landmarker_lite.task')

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        return self.detector.detect(mp_image)

