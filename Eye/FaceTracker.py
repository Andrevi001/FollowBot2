import config
import math

class FaceTracker():
    def __init__(self):
        self.width = config.width
        self.height = config.height

    def processFaces(self, faces):
        for face in faces:
            x, y, w, h = face[0:4].astype(int)
            confidence = face[14]
                        
            if confidence >= 0.7:                
                error_x = (x + w/2 - config.width/2) / (config.width/2)
                error_y = (y + h/2 - config.height/2) / (config.height/2)
                            
                pan = 0
                tilt = 0
        
                if abs(error_x) > config.dead_zone:
                    pan = int(error_x * config.Kgain)
        
                if abs(error_y) > config.dead_zone:
                    tilt = int(error_y * config.Kgain)

                distanza = self._calcolaDistanza(w,h)

                return 80, pan, tilt, distanza, (x, y, w, h)
        
        return 65, 0, 0, 0, (0, 0, 0, 0)

    def _calcolaDistanza(self, w: int, h: int) -> int:
        areaFrame = config.width * config.height
        areaBBox = w * h
        area = math.sqrt(areaBBox/areaFrame)
        return min(int((config.Kdistanza/area)*100),255)
