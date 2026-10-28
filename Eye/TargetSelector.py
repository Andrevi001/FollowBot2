import config
from Point import Point
import math
from PoseDistance import PoseDistance
from Identifier import Identifier

class TargetSelector:
    """Class designed to select the tracking target"""

    def __init__(self, identifier: Identifier, threshold: float):
        """Class constructor"""
        self.__center = Point(0.5, 0.5, 0)
        self.__identifier = identifier
        self.__threshold = threshold
    
    def enroll(self, samples):
        enrollement = []
        for poses, frame in samples:
            min_distance = math.inf
            min_pose = []
            for pose in poses:
                distance_from_center = self._pose_distance_from_center(pose)
                if distance_from_center < min_distance:
                    min_distance = distance_from_center
                    min_pose = pose
            
            enrollement.append((min_pose, frame))
        
        self.__identifier.enroll(enrollement)
            

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
            
            distance_from_center = self._pose_distance_from_center(pose)
            
            if self.__identifier.verify((pose, frame)) > self.__threshold:
                filtered_poses.append(PoseDistance(pose, distance_from_center))
        
        if not filtered_poses:
            return None
        else:
            filtered_poses.sort()
            return filtered_poses[0].pose
        
    def _pose_distance_from_center(self, pose):
        """
        Used to calculate the distance between the pose and the center of the frame.
        The calculated distance is in pixels so it depends on the camera resolution (config.width, config.height.)
            
        Args:
            pose: List of Point, pose keypoints.
        Returns:
            distance in pixels between pose and the center of the frame.
        """
        
        shoulder_l = pose[11]
        shoulder_r = pose[12]
        
        pose_center = Point((shoulder_r.x + shoulder_l.x)/2, (shoulder_r.y + shoulder_l.y)/2, 0)
        
        return math.dist([pose_center.x * config.width, pose_center.y * config.height], [self.__center.x * config.width, self.__center.y * config.height])