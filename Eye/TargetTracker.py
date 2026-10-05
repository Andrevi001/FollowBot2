import config
from Point import Point
from PID import PID
import math

class TargetTracker():
    """Class designed for continuous tracking of the target."""

    def __init__(self, K_neck_waist):
        """
        Class constructor

        Args:
            K_shoulders: constant to be used for distance calculation based on shoulder width.
            K_shoulder_elbow: constant to be used for distance calculation based on shoulder to elbow distance.
        """
        self.width = config.width
        self.height = config.height
        self.diagonal = math.sqrt((config.width**2) + (config.height**2))
        self.k_neck_waist = K_neck_waist
        self.pid_pan = PID(0.077, 0.002, 0.002)
        self.pid_tilt = PID(0.065, 0.0025, 0.001)
        self.deadZone = 0.04

    def processTargets(self, targets):
        """
        Used to calculate distance and position PID for each target.
        This also returns secondary information such as center of targeting and two Point for each target.
        The two returned points locate the base of the neck and the center of the waist.

        Args:
            targets: List of pose keypoints for each detected target.

        Returns:
            tuple: (trackingInfo, secondaryInfo)
            - trackingInfo: distance and PID for each target.
            - secondaryInfo: contains secodary information, center and the two Point for each target.
        """

        trackingInfo = []
        secondaryInfo = []

        if not targets:
            return (trackingInfo, secondaryInfo)

        for target in targets:
            shoulder_l = target[11]
            shoulder_r = target[12]
            waist_l = target[23]
            waist_r = target[24]
            
            error_x = 0
            error_y = 0
            center = ()
            distance = 0

            neck_base = Point((shoulder_r.x + shoulder_l.x) / 2.0, (shoulder_r.y + shoulder_l.y) / 2.0, (shoulder_r.visibility + shoulder_l.visibility) / 2.0)
            waist_center = Point((waist_r.x + waist_l.x) / 2.0, (waist_r.y + waist_l.y) / 2.0, (waist_r.visibility + waist_l.visibility) / 2.0)

            error_x = neck_base.x - 0.5
            error_y = neck_base.y - 0.5
            center = (int(neck_base.x * config.width), int(neck_base.y * config.height))
            distance = self._calculate_target_distance(neck_base, waist_center, self.k_neck_waist)
            
            pan = 0
            if abs(error_x) > self.deadZone: 
                pan = int(round(self.pid_pan.calculatePID(error_x) * 53))    

            tilt = 0
            if abs(error_y) > self.deadZone:
                tilt = int(round(self.pid_tilt.calculatePID(error_y) * 42))

            trackingInfo.append((pan, tilt, int(distance * 100)))
            secondaryInfo.append((center, neck_base, waist_center))

        return (trackingInfo, secondaryInfo)

    def _calculate_target_distance(self, point_a, point_b, k_distance) -> float:
        """
        Used to calculate the distance of the target. 
        The calculation based on the distance between two pose keypoints (point_a, point_b)  and their relation with the constant (k_distance).

        Args:
            point_a: Point, the first point.
            point_b: Point, the second point.
            k_distance: distant measurement constant.
        
        Returns:
            float: calculated distance to the target
        """

        if point_a.visibility < 0.4 or point_b.visibility < 0.4:
            return 0.21

        distance_p = self._calculate_distance(point_a, point_b)
        k_relative = k_distance * self.diagonal

        if distance_p == 0:
            return 0

        return k_relative / distance_p

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