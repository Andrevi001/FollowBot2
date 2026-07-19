#include <ESP32Servo.h>

const u_int8_t PAN = 26;
const u_int8_t TILT = 25;

Servo servoPan;
Servo servoTilt;

struct Pan_Tilt {
    private:
        int16_t pan = 85;
        int16_t tilt = 30;

    public:
        void centerFov() {
            pan = 85;
            tilt = 30;
            servoPan.write(pan);
            servoTilt.write(tilt);
        }

        void updateServos(int8_t pan_sum, int8_t tilt_sum) {
            pan += pan_sum;
            tilt += tilt_sum;

            servoPan.write(pan);
            servoTilt.write(tilt);
        }

        int16_t getPan() {
            return pan;
        }

        int16_t getTilt() {
            return tilt;
        }
}pt;