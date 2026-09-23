import config
from DistanceLogger import DistanceLogger
from PID import PID
import math

class TargetTracker():
    """Class designed for continuous tracking of the target."""

    def __init__(self, K_shoulders, K_shoulder_elbow):
        """
        Class constructor

        Args:
            K_shoulders: constant to be used for distance calculation based on shoulder width.
            K_shoulder_elbow: constant to be used for distance calculation based on shoulder to elbow distance.
        """
        self.width = config.width
        self.height = config.height
        self.diagonal = math.sqrt((config.width**2) + (config.height**2))
        self.k_shoulders = K_shoulders
        self.k_shoulder_elbow = K_shoulder_elbow
        self.pid_pan = PID(0.77, 0.005, 0.04)
        self.pid_tilt = PID(0.07, 0.003, 0.000005)
        self.deadZone = 0.04

    def processTargets(self, targets):
        """
        Used to calculate position, distance and PID for each target.
        This also returns secondary information such as center of the targeting and three TargetDetector.Point for each target.
        The 3 returned points locate the shoulders and the right elbow.

        Args:
            targets: List of pose keypoints for each detected target.

        Returns:
            tuple: (trackingInfo, secondaryInfo)
            - trackingInfo: contains position, distance and PID for each target.
            - secondaryInfo: contains secodary information, center and the three keypoints for each target.
        """

        trackingInfo = []
        secondaryInfo = []

        if not targets:
            return (trackingInfo, secondaryInfo)

        for target in targets:
            shoulder_l = target[11]
            shoulder_r = target[12]
            elbow_l = target[14]
            elbow_r = target[13]
                        
            if shoulder_l.visibility >= 0.5 or shoulder_r.visibility >= 0.5:

                error_x = 0
                error_y = 0
                center = ()
                distance = 0
                if shoulder_l.visibility < 0.5:
                    error_x = shoulder_r.x - 0.5
                    error_y = shoulder_r.y -0.62
                    center = (int(shoulder_r.x * config.width), int(shoulder_r.y * config.height))
                    distance = self._calculate_target_distance(shoulder_r, elbow_r, self.k_shoulder_elbow)
                elif shoulder_r.visibility < 0.5:
                    error_x = shoulder_l.x - 0.5
                    error_y = shoulder_l.y -0.62
                    center = (int(shoulder_l.x * config.width), int(shoulder_l.y * config.height))
                    distance = self._calculate_target_distance(shoulder_l, elbow_l, self.k_shoulder_elbow)
                else:
                    neck_base_x = (shoulder_r.x + shoulder_l.x) / 2.0
                    neck_base_y = (shoulder_r.y + shoulder_l.y) / 2.0

                    error_x = neck_base_x - 0.5
                    error_y = neck_base_y - 0.62
                    center = (int(neck_base_x * config.width), int(neck_base_y * config.height))
                    distance = self._calculate_target_distance(shoulder_l, shoulder_r, self.k_shoulders)
                
                pan = 0
                if abs(error_x) > self.deadZone: 
                    pan = int(round(self.pid_pan.calculatePID(error_x) * 53))    

                tilt = 0
                if abs(error_y) > self.deadZone:
                    tilt = int(round(self.pid_tilt.calculatePID(error_y) * 42))

                trackingInfo.append((80, pan, tilt, int(distance * 100)))
                secondaryInfo.append((center, shoulder_l, shoulder_r, elbow_r))

        return (trackingInfo, secondaryInfo)

    def _calculate_target_distance(self, point_a, point_b, k_distance) -> float:
        """
        Used to calculate the distance of the target. 
        The calculation based on the distance between two pose keypoints (point_a, point_b)  and their relation with the constant (k_distance).

        Args:
            point_a: TargetDetector.Point, the first point.
            point_b: TargetDetector.Point, the second point.
            k_distance: distant measurement constant.
        
        Returns:
            float: calculated distance to the target
        """

        if point_a.visibility < 0.5 or point_b.visibility < 0.5:
            return 2.56

        distance_p = self._calculate_distance(point_a, point_b)
        k_relative = k_distance * self.diagonal

        if distance_p == 0:
            return 0

        return k_relative / distance_p

    def _calculate_distance(self, point_a, point_b):
        """
        Used to calculate the distance between two given TargetDetector.Point.
        The calculated distance is in pixels so it depends on the camera resolution (config.width, config.height.)

        Args:
            point_a: TargetDetector.Point, the first point.
            point_b: TargetDetector.Point, the second point.
        
        Returns:
            distance in pixels between point_a and point_b.
        """

        return math.dist([point_a.x * config.width, point_a.y * config.height], [point_b.x * config.width, point_b.y * config.height])