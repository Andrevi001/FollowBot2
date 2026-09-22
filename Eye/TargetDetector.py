import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import threading

class TargetDetector:
    """Class for asynchronous target detection using MediaPipe PoseLandmarker."""

    class Point:
        """Internal class that defines a 2D point and it's visibilty"""

        def __init__(self, x, y, visibility):
            self.x = x
            self.y = y
            self.visibility = visibility

    def __init__(self):
        """Class constructor"""

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
        """
        Used to start an asynchronous target detection on the given frame
        
        Args:
            frame: numpy.array on which to process the target detection.
        """
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        
        timestamp = int(time.perf_counter() * 1000)
        self.detector.detect_async(mp_image, timestamp)


    def _internal_callback(self, result, _output_image, _timestamp_ms):
        """
        Used as an internal callback for the asynchronous detection, required by self.detector

        Args:
            result: detection results, pose_landmarks and pose_world_landmarks.
            _output_image: the original frame on which the target detection was processed.
            _timestamp_ms: time stamp in ms of the original frame.        
        """

        targets = []

        if result.pose_landmarks:
            for person_landmarks in result.pose_landmarks:
                pose = []
                for kps in person_landmarks:
                    pose.append(self.Point(kps.x, kps.y, kps.visibility))

                targets.append(pose)

        with self._lock:
            self.__new_targets = targets
            self.__new_data = True

    def get_Targets(self):
        """
        Used to obtain the targets pose information

        Returns:
            List of Point or None, list that countains the key points of the detected poses in the frame, None if there's no new data 
        """
        with self._lock:
            if self.__new_data:
                self.__new_data = False
                return self.__new_targets
            return None

    def close(self):
        """Used to safely close this instance of the class"""

        self.detector.close()
