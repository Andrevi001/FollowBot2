from Identifier import Identifier
from Point import Point
import numpy as np
import math
import config
import cv2

side = 100



class ChromaticIdentifier(Identifier):
    def __init__(self, portion):
        """
        Class constructor

        Args:
            pixels: value between 0 and 1 that indicates the portion of the frame to be used as a feature extraction region.
                    the region is a square that covers part of the torso area.
        
        """
        self.__id = None
        self.__portion = portion
    
    def enroll(self, samples):
        mean_colors = []
        for pose, frame in samples:
            mean_color = self._calculate_mean_color(pose, frame)
            
            if mean_color is not None:
                mean_colors.append(mean_color)
        
        self.__id = np.mean(mean_colors, axis=0)

    def verify(self, sample):
        
        if self.__id is None:
            return -1
        
        pose, frame = sample
        subject_mean_color = self._calculate_mean_color(pose, frame)
        if subject_mean_color is None:
            return -2
        
        comparison = []
        for identity, subject in zip(self.__id, subject_mean_color):
            lesser = min(identity, subject)
            greater = max(identity, subject)
            
            if greater == 0:
                comparison.append(1-lesser/255)
            else:
                comparison.append(lesser/greater)
            
        return np.mean(comparison)
        


    def _calculate_mean_color(self, pose, frame):
        """
        Calculates the mean color of the pose in the frame.
        The average is calculated over the torso region of the pose. 
        The size of the region depends on the subjects distance.
        
        Args:
            pose: List of Point that contains the pose keypoints.
            frame: numpy.array, frame that is relative to the given keypoints.
        Returns:
            numpy.array that contains the average color in RGB format, [R, G, B]
        """

        shoulder_l = pose[11]
        shoulder_r = pose[12]
            
        shoulder_center = Point((shoulder_l.x + shoulder_r.x)/2, (shoulder_l.y + shoulder_r.y)/2 + 0.05, (shoulder_l.visibility + shoulder_r.visibility)/2)

        distance = self._calculate_distance(shoulder_l, shoulder_r)
        pixels = int(round(distance*self.__portion))

        half = pixels // 2
        x = int(shoulder_center.x * config.width)
        y = int(shoulder_center.y * config.height)
        top_left = (x - half, y - half)
        bottom_right = (x + half, y + half)
        if frame is not None:
            img = frame.numpy_view().copy()
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            cv2.imshow("camera", img)
            cv2.waitKey(1)


        cropped_frame = self._crop_around(frame, shoulder_center, pixels)
        
        if cropped_frame is None:
            return None
        
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
