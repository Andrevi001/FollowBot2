from Identifier import Identifier
from Point import Point
import numpy as np
from DistanceLogger import DistanceLogger
import math
import config

class ChromaticIdentifier(Identifier):
    def __init__(self):
        self.__id = None
    
    def enroll(self, samples):
        mean_colors = []
        for pose, frame in samples:
            mean_color = self._calculate_mean_color(pose, frame)
            mean_colors.append(mean_color)
        
        self.__id = np.mean(mean_colors, axis=0)

    def verify(self, sample):
        
        if self.__id is None:
            return -1
        
        pose, frame = sample
        subject_mean_color = self._calculate_mean_color(pose, frame)
        comparison = []
        for identity, subject in zip(self.__id, subject_mean_color):
            lesser = min(identity, subject)
            greater = max(identity, subject)
            
            if greater == 0:
                comparison.append(1-lesser/255)
            else:
                comparison.append(lesser/greater)
            
        return np.mean(comparison)
        


    def _calculate_mean_color(self, pose,frame):
        """
        Calculates the mean color of the pose in the frame.
        The average is calculated over the torso region of the pose. 
        The size of the region depends on the subjects distance.
        
        Args:
            pose: List of Point that contains the pose keypoints.
            frame: numpy.array, frame that is relative to the given keypoints.
        Returns:
            numpy.array that contains the average color in BGR format, [B, G, R]
        """

        shoulder_l = pose[11]
        shoulder_r = pose[12]
        hip_l = pose[23]
        hip_r = pose[24]

            
        shoulder_center = Point((shoulder_l.x + shoulder_r.x)/2, (shoulder_l.y + shoulder_r.y)/2, (shoulder_l.visibility + shoulder_r.visibility)/2)
        hip_center = Point((hip_l.x + hip_r.x)/2, (hip_l.y + hip_r.y)/2, (hip_l.visibility + hip_r.visibility)/2)
        center = Point((shoulder_center.x + hip_center.x)/2, (shoulder_center.y + hip_center.y)/2, (shoulder_center.visibility + hip_center.visibility)/2)

        distance = self._calculate_distance(shoulder_l, shoulder_r)
        pixels = int(round(distance*0.10))

        cropped_frame = self.crop_around(frame, center, pixels)
        
        return  np.mean(cropped_frame, axis=(0, 1))
        

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
        
        height, width = frame.shape[:2]
        half = length // 2

        x = center.x * config.width
        y = center.y * config.height

        x1 = max(0, int(x - half))
        x2 = min(width, int(x + half))

        y1 = max(0, int(y - half))
        y2 = min(height, int(y + half))

        return frame[y1:y2, x1:x2]
    
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
