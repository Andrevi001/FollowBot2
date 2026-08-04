import config
from DistanceLogger import DistanceLogger

class TargetTracker():
    def __init__(self):
        self.width = config.width
        self.height = config.height
        self.log = DistanceLogger("Distance/K_spalle.txt", "Distance/K_spalla_gomito.txt")

    def processTargets(self, targets):

        landmarks = []

        if not targets:
            return landmarks

        for target in targets:
            spalla_s = target[11]
            spalla_d = target[12]
                        
            if spalla_s.visibility >= 0.5 or spalla_d.visibility >= 0.5:

                error_x = 0
                error_y = 0
                center = ()
                if spalla_s.visibility < 0.5:
                    error_x = spalla_d.x - 0.5
                    error_y = spalla_d.y -0.45
                    center = (int(spalla_d.x * config.width), int(spalla_d.y * config.height))
                elif spalla_d.visibility < 0.5:
                    error_x = spalla_s.x - 0.5
                    error_y = spalla_s.y -0.45
                    center = (int(spalla_s.x * config.width), int(spalla_s.y * config.height))
                else:
                    base_collo_x = (spalla_d.x + spalla_s.x) / 2.0
                    base_collo_y = (spalla_d.y + spalla_s.y) / 2.0

                    error_x = base_collo_x - 0.5
                    error_y = base_collo_y - 0.45
                    center = (int(base_collo_x * config.width), int(base_collo_y * config.height))

                self.log.add_spalle_distance(spalla_s,spalla_d)
                gomito_s = target[14]
                self.log.add_spalla_gomito_distance(spalla_s, gomito_s)
                     
                pan = 0
                tilt = 0
        
                if abs(error_x) > config.dead_zone:
                    pan = int(error_x * config.Kgain)
        
                if abs(error_y) > config.dead_zone:
                    tilt = int(error_y * config.Kgain)

                landmarks.append((80, pan, tilt, 150, center))

        return landmarks

    def _calcolaDistanzaSpalle(self, spalla_s, spalla_d) -> int:
        return

    def _calcolaDistanzaSpallaGomito(self, spalla, gomito) -> int:
        return