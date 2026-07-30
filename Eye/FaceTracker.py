import config
import math

class FaceTracker():
    def __init__(self):
        self.width = config.width
        self.height = config.height

    def processFaces(self, faces):
        for face in faces:
            confidence = face.categories[0].score if face.categories else 0.0
                        
            if confidence >= 0.2:
                bbox = face.bounding_box
                error_x = (bbox.origin_x + bbox.width/2 - config.width/2) / (config.width/2)
                error_y = (bbox.origin_y + bbox.height/2 - config.height/2) / (config.height/2)
                            
                pan = 0
                tilt = 0
        
                if abs(error_x) > config.dead_zone:
                    pan = int(error_x * config.Kgain)
        
                if abs(error_y) > config.dead_zone:
                    tilt = int(error_y * config.Kgain)

                distanza = self._calcolaDistanza(bbox.width, bbox.height)

                return 80, pan, tilt, distanza, (bbox.origin_x, bbox.origin_y, bbox.width, bbox.height)
        
        return 65, 0, 0, 0, (0, 0, 0, 0)

    def _calcolaDistanza(self, w: int, h: int) -> int:
        areaFrame = config.width * config.height
        areaBBox = w * h
        area = math.sqrt(areaBBox/areaFrame)
        return min(int((config.Kdistanza/area)*100),255)
