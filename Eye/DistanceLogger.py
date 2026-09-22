import os
import config
import math

class DistanceLogger:
    """Class used to log body measurments used to calculate the distance form the target"""
    def __init__(self, path1, path2):
        """Class Constructor"""
        self.__shoulder_path = path1
        self.__shoulder_elbow_path = path2
        self.__k_shoulders = 0.0
        self.__k_shoulder_elbow = 0.0
        self.update_K()
    
    def add_shoulders_distance(self, shoulder_l, shoulder_r):
        """
        Used to log a new shoulder to shoulder distance

        Args:
            shoulder_l: TargetDetector.Point that contains the coordinates of the left shoulder
            shoulder_l: TargetDetector.Point that contains the coordinates of the right shoulder

        """

        distance = math.dist([shoulder_l.x * config.width, shoulder_l.y * config.height], [shoulder_r.x * config.width, shoulder_r.y * config.height])
        with open(self.__shoulder_path, "a") as file:
            file.write(f"{distance}\n")


    def add_shoulder_elbow_distance(self, shoulder, elbow):
        """
        Used to log a new shoulder to elbow distance
        
        Args:
            shoulder: TargetDetector.Point that contains the coordinates of the shoulder
            elbow: TargetDetector.Point that contains the coordinates of the elbow
        
        """

        distance = math.dist([shoulder.x * config.width, shoulder.y * config.height], [elbow.x * config.width, elbow.y * config.height])
        with open(self.__shoulder_elbow_path, "a") as file:             
            file.write(f"{distance}\n")


    def K_shoulders(self) -> float:
        """
        Used to obtain K_shoulders

        Args:
            float: constant calculatedbased on the entries of self.__Shoulder_path
        """
        return self.__k_shoulders 

    def K_shoulder_elbow(self) -> float:
        """
        Used to obtain K_shoulders
        
        Args:
            float: constant calculatedbased on the entries of self.__Shoulder_path
        """  
        return  self.__k_shoulder_elbow

    def update_K(self):
        """Used to update self.__k_shoulders and self.__k_shoulder_elbow values with information contained in self.__shoulder_path and self.__shoulder_elbow_path"""

        diagonal = math.sqrt((config.width**2) + (config.height**2))

        self.__k_shoulders = self._averageDistance(self.__shoulder_path) / diagonal
        self.__k_shoulder_elbow = self._averageDistance(self.__shoulder_elbow_path) / diagonal

    def _averageDistance(self, filePath):
        """
        Used to calculate the average distance contained in filePath

        Args:
            filePath: string that pints to the file that contains a set of distances
        """
        file_exists = os.path.exists(filePath)
        
        if not file_exists:
            return 0.0

        sum = 0.0
        n = 0
        with open(filePath, "r") as file:
            for line in file:
                sum = sum + float(line.strip())
                n = n + 1

        if n == 0:
            return 0
        
        return sum / n
