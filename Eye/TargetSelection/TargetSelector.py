import config
from Point import Point
import math
from TargetSelection.PoseDistance import PoseDistance
from Identifier.Identifier import Identifier
from Identifier.Verdict import Verdict

class TargetSelector:
    """Class designed to select the tracking target"""

    def __init__(self, identifier1: Identifier, identifier2: Identifier):
        """
        Class constructor
        
        Args:
            identifier1: First Identifier to filter the possible targets
            identifier2: Second Identifier to filter the possible targets
        """
        
        self.__center = Point(0.5, 0.5, 0)
        self.__identifier1 = identifier1
        self.__identifier2 = identifier2
    
    def enroll(self, samples):
        """
        Used to extract and store identifiying data
        
        Args:
            samples: List of tuple(list(list(Point)), list(mp.image))
        """
        
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
        
        self.__identifier1.enroll(enrollement)
        self.__identifier2.enroll(enrollement)

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
            verdict = self.__identifier1.verify((pose, frame))
            
            if verdict == Verdict.MATCH:
                filtered_poses.append(PoseDistance(pose, distance_from_center))
        
        second_filter = []
        for pose_and_distance in filtered_poses:
            verdict = self.__identifier2.verify((pose_and_distance.pose, frame))
            
            if verdict == Verdict.MATCH:
                second_filter.append(pose_and_distance)
        
        if not second_filter and not filtered_poses:
            return None
        elif second_filter:
            second_filter.sort()
            return second_filter[0].pose
        elif filtered_poses:
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