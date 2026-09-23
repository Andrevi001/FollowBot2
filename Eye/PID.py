import time

class PID():

    """Class designed to calcultare the PID for the Pan/Tilt mechanism"""

    def __init__(self, Kp, Ki, Kd):
        """
        Class Constructor
        
        Args:
            Kp: proportional constant for PID calculation
            Ki: integral constant for PID calculation
            Kd: derivative constant for PID calculation
        """

        self.oldTime = time.perf_counter()
        self.oldError = 0
        self.integralError = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def calculatePID(self, error):
            """
            Calculates PID given a certain error.

            Args:
                error: value on which to calculate the PID 
            """

            now = time.perf_counter()
            deltaT = now-self.oldTime

            self.integralError = self.integralError + (error * deltaT)
            derivative = (error - self.oldError) / deltaT
            self.oldError = error
            self.oldTime = now
    
            P = self.Kp * error
            I = self.Ki * self.integralError
            D = self.Kd * derivative
    
            return P+I+D