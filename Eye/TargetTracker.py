import config
from DistanceLogger import DistanceLogger
from PIDPanTilt import PIDPanTilt
import math

class TargetTracker():
    """Class designed for continuos tracking of the target."""

    def __init__(self):
        """Class constructor"""
        self.width = config.width
        self.height = config.height
        self.log = DistanceLogger("Distance/K_Shoulders.txt", "Distance/K_Shoulder_Elbow.txt")
        self.pid = PIDPanTilt()
        self.deadZone = 0.04

    def processTargets(self, targets):
        """
        Used to calculate the targets position

        Args:
            targets: list of TargetDetector.Pointt, source of the targets pose keypointts.
        """

        landmarks = []

        if not targets:
            return landmarks

        for target in targets:
            shoulder_l = target[11]
            shoulder_r = target[12]
                        
            if shoulder_l.visibility >= 0.5 or shoulder_r.visibility >= 0.5:

                error_x = 0
                error_y = 0
                center = ()
                distance = 0
                if shoulder_l.visibility < 0.5:
                    error_x = shoulder_r.x - 0.5
                    error_y = shoulder_r.y -0.62
                    center = (int(shoulder_r.x * config.width), int(shoulder_r.y * config.height))
                    elbow_r = target[13]
                    distance = self._calcolateDistanceUsingShoulderAndElbow(shoulder_r, elbow_r)
                elif shoulder_r.visibility < 0.5:
                    error_x = shoulder_l.x - 0.5
                    error_y = shoulder_l.y -0.62
                    center = (int(shoulder_l.x * config.width), int(shoulder_l.y * config.height))
                    elbow_l = target[14]
                    distance = self._calcolateDistanceUsingShoulderAndElbow(shoulder_l, elbow_l)
                else:
                    neck_base_x = (shoulder_r.x + shoulder_l.x) / 2.0
                    neck_base_y = (shoulder_r.y + shoulder_l.y) / 2.0

                    error_x = neck_base_x - 0.5
                    error_y = neck_base_y - 0.62
                    center = (int(neck_base_x * config.width), int(neck_base_y * config.height))
                    distance = self._calcolateDistanceUsingShoulders(shoulder_l, shoulder_r)

                # Remove to add new body part distnace in memory. warning: target has to stay still and be at 100cm form the rover.
                #self.log.add_spalle_distance(shoulder_l,shoulder_r)
                #elbow_l = target[14]
                #self.log.add_shoulder_gomito_distance(shoulder_l, elbow_l)
                
                pan = 0
                if abs(error_x) > self.deadZone: 
                    pan = int(round(self.pid.calculatePID(error_x, 0) * 53))    

                tilt = 0
                if abs(error_y) > self.deadZone:
                    tilt = int(round(self.pid.calculatePID(error_y, 1) * 42))

                landmarks.append((80, pan, tilt, int(distance * 100), center))

        return landmarks

    def _calcolateDistanceUsingShoulders(self, shoulder_l, shoulder_r) -> float:
        """
        Used to calculate the distance of the target based on shoulder to shoulder distance.

        Args:
            shoulder_l: TargetDetector.Point, left shoulder coordinates.
            shoulder_r: TargetDetector.Point, right shoulder coordinates.
        
        Returns:
            float: calculated distance to the target
        """
        distance_p = math.dist([shoulder_l.x * config.width, shoulder_l.y * config.height], [shoulder_r.x * config.width, shoulder_r.y * config.height])
        diagonal = math.sqrt((config.width**2) + (config.height**2))
        k_relative = self.log.K_shoulders() * diagonal

        if distance_p == 0:
            return 0

        return k_relative / distance_p

    def _calcolateDistanceUsingShoulderAndElbow(self, shoulder, elbow) -> float:
        """
        Used to calculate the distance of the target based on shoulder to elbow distance.
        
        Args:
            shoulder: TargetDetector.Point, shoulder coordinates.
            elbow: TargetDetector.Point, elbow coordinates.
                
        Returns:
            float: calculated distance to the target
        """
        if elbow.visibility < 0.5:
            return 2.56

        distance_p = math.dist([shoulder.x * config.width, shoulder.y * config.height], [elbow.x * config.width, elbow.y * config.height])
        diagonal = math.sqrt((config.width**2) + (config.height**2))
        
        if distance_p == 0:
            return 0

        return (self.log.K_shoulder_elbow()*diagonal) / distance_p