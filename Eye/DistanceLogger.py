import os
import config
import math

class DistanceLogger:
    """Class used to log body measurements used to calculate the distance from the target"""
    def __init__(self, path):
        """Class Constructor"""
        self.__file_path = path
        self.__k_distance = 0.0
        self.__distance_log = []
        self.update_K()
    
    def add_distance(self, point_a, point_b):
        """
        Used to add a new distance,must be used with write to file to save measurments.

        Args:
            point_a: TargetDetector.Point that contains the coordinates of the first point
            point_b: TargetDetector.Point that contains the coordinates of the second point

        """

        distance = math.dist([point_a.x * config.width, point_a.y * config.height], [point_b.x * config.width, point_b.y * config.height])
        self.__distance_log.append(distance)


    def K_distance(self) -> float:
        """
        Used to obtain distance constant

        Returns:
            float: constant calculated based on the entries of self.__file_path
        """
        return self.__k_distance

    def update_K(self):
        """Used to update self.__k_distance value with information contained in self.__file_path"""

        self.__k_distance = self._averageDistance(self.__file_path)

    def _averageDistance(self, filePath):
        """
        Used to calculate the average distance contained in filePath

        Args:
            filePath: string that points to the file that contains a set of distances
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

    def writeToFile(self):
        """
        Used to save new distance measurments to self.__file_path, to be used at the end of the program.
        """
        diagonal = math.sqrt((config.width**2) + (config.height**2))
        with open(self.__file_path, "a") as file:
            for distance in self.__distance_log:
                file.write(f"{distance/diagonal}\n")

        self.__distance_log = []
        self.update_K()
