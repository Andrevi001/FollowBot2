import time

class PIDPanTilt():
    def __init__(self):
        self.oldTime = 0
        self.oldError_x = 0
        self.integralError_x = 0
        self.Kpx = 0.077
        self.Kix = 0.005
        self.Kdx = 0.004
        self.oldError_y = 0
        self.integralError_y = 0
        self.Kpy = 0.07
        self.Kiy = 0.003
        self.Kdy = 0.000005

    def calculatePID(self, error, selection):
            integralError = 0
            derivative = 0
            now = time.perf_counter()
            deltaT = now-self.oldTime
    
            if selection == 0:
                if self.oldTime != 0:
                    integralError = self.integralError_x + (error*deltaT)
                if self.oldError_x != 0:
                    derivative = (error - self.oldError_x) / deltaT
                self.integralError_x = integralError
                self.oldError_x = error
                Kp = self.Kpx
                Ki = self.Kix
                Kd = self.Kdx 
            else:
                if self.oldTime != 0:
                    integralError = self.integralError_y + (error*deltaT)
                if self.oldError_y != 0:
                    derivative = (error - self.oldError_y) / deltaT
                self.integralError_y = integralError
                self.oldError_y = error
                Kp = self.Kpy
                Ki = self.Kiy
                Kd = self.Kdy
    
            self.oldTime = now
    
            P = Kp * error
            I = Ki * integralError
            D = Kd * derivative
    
            return P+I+D