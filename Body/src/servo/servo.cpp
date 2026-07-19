#include "servo.h"

// Definiamo fisicamente i servi e l'oggetto pt (una sola volta nel progetto)
Servo servoPan;
Servo servoTilt;
Pan_Tilt pt;

void Pan_Tilt::centerFov() {
    pan = 85;
    tilt = 30;
    servoPan.write(pan);
    servoTilt.write(tilt);
}

void Pan_Tilt::updateServos(int8_t pan_sum, int8_t tilt_sum) {
    pan += pan_sum;
    tilt += tilt_sum;

    servoPan.write(pan);
    servoTilt.write(tilt);
}

int16_t Pan_Tilt::getPan() {
    return pan;
}

int16_t Pan_Tilt::getTilt() {
    return tilt;
}