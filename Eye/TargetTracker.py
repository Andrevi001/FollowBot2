import config
from DistanceLogger import DistanceLogger
import math

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
                distance = 0
                if spalla_s.visibility < 0.5:
                    error_x = spalla_d.x - 0.5
                    error_y = spalla_d.y -0.40
                    center = (int(spalla_d.x * config.width), int(spalla_d.y * config.height))
                    gomito_d = target[13]
                    distance = self._calcolaDistanzaSpallaGomito(spalla_d, gomito_d)
                elif spalla_d.visibility < 0.5:
                    error_x = spalla_s.x - 0.5
                    error_y = spalla_s.y -0.40
                    center = (int(spalla_s.x * config.width), int(spalla_s.y * config.height))
                    gomito_s = target[14]
                    distance = self._calcolaDistanzaSpallaGomito(spalla_s, gomito_s)
                else:
                    base_collo_x = (spalla_d.x + spalla_s.x) / 2.0
                    base_collo_y = (spalla_d.y + spalla_s.y) / 2.0

                    error_x = base_collo_x - 0.5
                    error_y = base_collo_y - 0.40
                    center = (int(base_collo_x * config.width), int(base_collo_y * config.height))
                    distance = self._calcolaDistanzaSpalle(spalla_s, spalla_d)

                # Togliere per aggiungere altri dati in memoria. Attenzione: verifcare che il bersaglio si trovi a 1M di distanza e che non si muova
                #self.log.add_spalle_distance(spalla_s,spalla_d)
                #gomito_s = target[14]
                #self.log.add_spalla_gomito_distance(spalla_s, gomito_s)
                     
                pan = 0
                tilt = 0
        
                #implementare un modo migliore per il calcolo pan/tilt. Possibilmente PID.

                landmarks.append((80, pan, tilt, int(distance * 100), center))

        return landmarks

    def _calcolaDistanzaSpalle(self, spalla_s, spalla_d) -> float:
        distance_p = math.dist([spalla_s.x * config.width, spalla_s.y * config.height], [spalla_d.x * config.width, spalla_d.y * config.height])
        diagonale_attuale = math.sqrt((config.width**2) + (config.height**2))
        k_relativo = self.log.K_spalle() * diagonale_attuale

        if distance_p == 0:
            return 0

        return k_relativo / distance_p

    def _calcolaDistanzaSpallaGomito(self, spalla, gomito) -> int:
        if gomito.visibility < 0.5:
            return 2.55

        distance_p = math.dist([spalla.x * config.width, spalla.y * config.height], [gomito.x * config.width, gomito.y * config.height])
        
        if distance_p == 0:
            return 0

        return self.log.K_spalla_gomito() / distance_p