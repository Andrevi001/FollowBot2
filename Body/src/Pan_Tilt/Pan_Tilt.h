#ifndef Pan_Tilt_H
#define Pan_Tilt_H

#include <ESP32Servo.h>

constexpr uint8_t PAN = 26;
constexpr uint8_t TILT = 25;

/**
 * Classe singoletto per la gestione del sistema Pan/Tilt.
 */
class Pan_Tilt {
    private:
        int16_t pan = 85;
        int16_t tilt = 30;

        Servo servoPan;
        Servo servoTilt;

        Pan_Tilt();
        Pan_Tilt(const Pan_Tilt&) = delete;
        Pan_Tilt& operator=(const Pan_Tilt&) = delete;

    public:

        static Pan_Tilt& getInstance() {
            static Pan_Tilt instance;
            return instance;
        }

        void begin();
        void centerFov();
        void updateServos(int8_t pan_sum, int8_t tilt_sum);
        int16_t getPan() const;
        int16_t getTilt() const;
}; 

#endif