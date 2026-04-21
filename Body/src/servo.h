#include <ESP32Servo.h>

const int PAN = 26;
const int TILT = 25;

Servo servoPan;
Servo servoTilt;

struct Pan_Tilt {
    private:
        int16_t pan = 85;
        int16_t tilt = 40;

    public:
        void centerFov() {
            pan = 85;
            tilt = 40;
            servoPan.write(pan);
            servoTilt.write(tilt);
        }

        void updateServos(int8_t pan_sum, int8_t tilt_sum) {
            pan += pan_sum;
            tilt += tilt_sum;

            pan = constrain(pan, 0, 180);
            tilt = constrain(tilt, 0, 180);

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