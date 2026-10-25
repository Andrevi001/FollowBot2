import config
from Point import Point
import math
from PoseDistance import PoseDistance
from Identifier import Identifier

class TargetSelector():
    """Class designed to select the tracking target"""

    def __init__(self, chromatic_identifier: Identifier, threshold: float):
        """Class constructor"""
        self.__center = Point(0.5, 0.5, 0)
        self.__chromatic_identifier = chromatic_identifier
        self.__threshold = threshold

    def select(self, poses, frame):
        """
        Used to parse the given poses and select the subject of tracking.
        The pose to be tracked will be the one whose similarity score exceeds the given threshold.
        The similarity score is calculated by the identifier.
        If more poses score above the threshold, the one to track will be the one closest to the center of the frame.
        
        Args:
            poses: List of List containing for each pose the corresponding landmarks

        Returns:
            pose: List of landmarks representing the selected pose.
        
        """
        filtered_poses = []
        for pose in poses:
            shoulder_l = pose[11]
            shoulder_r = pose[12]

            pose_center = Point((shoulder_r.x + shoulder_l.x)/2, (shoulder_r.y + shoulder_l.y)/2, 0)
            distance_from_center = self._calculate_distance(pose_center, self.__center)
            
            if self.__chromatic_identifier.verify(pose, frame) > self.__threshold:
                filtered_poses.append(PoseDistance(pose, distance_from_center))
        
        if not filtered_poses:
            return None
        else:
            filtered_poses.sort()
            return filtered_poses[0].pose
        
        

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