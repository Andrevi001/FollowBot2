import os
import config
import math

class DistanceLogger:
    def __init__(self, path1, path2):
        self.__spalle_path = path1
        self.__spalla_gomito_path = path2
        self.__k_spalle = 0.0
        self.__k_spalla_gomito = 0.0
        self.update_K()
    
    def add_spalle_distance(self, spalla_s, spalla_d):

        distance = math.dist([spalla_s.x * config.width, spalla_s.y * config.height], [spalla_d.x * config.width, spalla_d.y * config.height])
        with open(self.__spalle_path, "a") as file:
            file.write(f"{distance}\n")


    def add_spalla_gomito_distance(self, spalla, gomito):

        distance = math.dist([spalla.x * config.width, spalla.y * config.height], [gomito.x * config.width, gomito.y * config.height])
        with open(self.__spalla_gomito_path, "a") as file:             
            file.write(f"{distance}\n")


    def K_spalle(self) -> float:
       return self.__k_spalle 

    def K_spalla_gomito(self) -> float:  
        return  self.__k_spalla_gomito

    def update_K(self):
        diagonale = math.sqrt((config.width**2) + (config.height**2))

        self.__k_spalle = self._meanDistance(self.__spalle_path) / diagonale
        self.__k_spalla_gomito = self._meanDistance(self.__spalla_gomito_path) / diagonale

    def _meanDistance(self, filePath):
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
