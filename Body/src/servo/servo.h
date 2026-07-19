#ifndef SERVO_H
#define SERVO_H

#include <ESP32Servo.h>

constexpr uint8_t PAN = 26;
constexpr uint8_t TILT = 25;

extern Servo servoPan;
extern Servo servoTilt;

struct Pan_Tilt {
    private:
        int16_t pan = 85;
        int16_t tilt = 30;

    public:
        void centerFov();
        void updateServos(int8_t pan_sum, int8_t tilt_sum);
        int16_t getPan();
        int16_t getTilt();
}; 


extern Pan_Tilt pt;

#endif