from Identifier.Identifier import Identifier
import cv2
import numpy as np
from Point import Point
from Identifier.Verdict import Verdict
import math
import config

class FaceIdentifierLBPH(Identifier):
    def __init__(self, portion, threshold, id_size):
        """
        Class constructor

            Args:
                portion, threshold: same as Identifier.
                id_size : lenght of the side of the square identification region.
        """

        super().__init__(portion, threshold)
        self.__id_size = id_size
        self.__enrolled = False
        self.__recognizer = cv2.face.LBPHFaceRecognizer_create()
        
    def enroll(self, samples):
        
        gray_frames = []
        
        for sample in samples:

            gray_and_resized = self._preprocessing(gray_and_resized)
            gray_frames.append(gray_and_resized)
        
        labels = np.zeros(len(gray_frames), dtype=np.int32)
        
        self.__recognizer.train(gray_frames, labels)
        
        self.__enrolled = True
    
    def verify(self, sample):
        if not self.__enrolled:
            return Verdict.NOT_ENROLLED
        
        gray_and_resized = self._preprocessing(sample)
        
        label, distance = self.__recognizer.predict(gray_and_resized)
        
        max_distance = 4 * self.__recognizer.getGridX() * self.__recognizer.getGridY()
        similarity = 1 - distance/max_distance
        
        if similarity >= self._threshold:
            return Verdict.MATCH
        else:
            return Verdict.NO_MATCH
        
        
    def _preprocessing(self, sample):
        """
        Prepares the given for identification
        
            Args:
                sample: containing pose and corresponing frame
            
            Returns:
                square, grayscale region of self.__id_size dimensions 
        """
        
        pose, frame = sample
        
        nose = pose[0]
        ear_l = pose[7]
        ear_r = pose[8]
            
        padding = 50
        ear_to_ear_distance = self._calculate_distance(ear_l, ear_r)
            
        cropped_frame = self._crop_around(frame, nose, round(padding + ear_to_ear_distance))
            
        gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        height, width = gray_frame.shape

        gray_and_resized = gray_frame

        if height > self.__id_size:
            gray_and_resized = cv2.resize(gray_frame, (self.__id_size, self.__id_size), interpolation=cv2.INTER_AREA)
        elif width < self.__id_size:
            gray_and_resized = cv2.resize(gray_frame, (self.__id_size, self.__id_size), interpolation=cv2.INTER_LINEAR)
            
        return gray_and_resized 
    
    
    def _crop_around(self, frame, center: Point, length: int):
        """
        Crops a square with the specified side length, centered around the given point in the frame.
        
        Args:
            frame: numpy.array to be cropped
            center: Point center of the cropping, normalized value relative to frame.
            length: length of the square's side, measured in pixels.
        Returns:
            numpy.array containing the cropped area
        """

        img = frame.numpy_view()
        h, w = img.shape[:2]

        x = round(center.x * w) - length // 2
        y = round(center.y * h) - length // 2
        x1, y1 = x + length, y + length

        if x < 0 or y < 0 or x1 > w or y1 > h:
            return None

        return img[y:y1, x:x1]

    def _calculate_distance(self, point_a, point_b):
        """
        Used to calculate the distance between two given Point.
        The calculated distance is in pixels so it depends on the camera resolution (config.width, config.height.)
    
        Args:
            point_a: Point, the first point.
            point_b: Point, the second point.
        
        Returns:
            distance in pixels between point_a and point_b.
        """
    
        return math.dist([point_a.x * config.width, point_a.y * config.height], [point_b.x * config.width, point_b.y * config.height])
