import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import threading

class TargetDetector:

    class Punto:
        def __init__(self, x, y, visibility):
            self.x = x
            self.y = y
            self.visibility = visibility

    def __init__(self):
        self.__new_targets = []
        self.__new_data = False
        self._lock = threading.Lock()
        base_options = python.BaseOptions(model_asset_path='Modelli/pose_landmarker_lite.task')

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self._internal_callback
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect_async(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        
        timestamp = int(time.perf_counter() * 1000)
        self.detector.detect_async(mp_image, timestamp)


    def _internal_callback(self, result, _output_image, _timestamp_ms):
        targets = []

        if result.pose_landmarks:
            for person_landmarks in result.pose_landmarks:
                pose = []
                for kps in person_landmarks:
                    pose.append(self.Punto(kps.x, kps.y, kps.visibility))

                targets.append(pose)

        with self._lock:
            self.__new_targets = targets
            self.__new_data = True

    def get_Targets(self):
        with self._lock:
            if self.__new_data:
                self.new_data = False
                return self.__new_targets
            return []
