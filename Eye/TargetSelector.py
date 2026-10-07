import config
from Point import Point
import math

class TargetSelector():
    """Class designed to select the tracking target"""

    def __init__(self):
        """Class constructor"""
        self.__center = Point(0.5, 0.5, 0)

    def select(self, poses):
        """
        Used to parse the given poses and select the subject of tracking.
        The target will be the pose that is closest to the center of the frame.
        
        Args:
            poses: List of Lists containg for each pose the relative landmarks

        Returns:
            target: List containg the targets pose landmarks.
        
        """
        
        closest = None
        min_distance = math.inf
        for target in poses:
            shoulder_l = target[11]
            shoulder_r = target[12]

            pose_center = Point((shoulder_r.x + shoulder_l.x)/2, (shoulder_r.y + shoulder_l.y)/2, 0)
            distance_from_center = self._calculate_distance(pose_center, self.__center)

            if distance_from_center < min_distance:
               closest = target
               min_distance = distance_from_center

        return closest 

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