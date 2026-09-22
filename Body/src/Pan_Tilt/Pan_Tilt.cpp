#include "Pan_Tilt.h"

Pan_Tilt::Pan_Tilt() {}

/**
 * Function used to center the FOV
 */
void Pan_Tilt::centerFov() {
    pan = 85;
    tilt = 30;
    servoPan.write(pan);
    servoTilt.write(tilt);
}

/**
 * Function used to initialize the system
 */
void Pan_Tilt::begin() {
    servoPan.attach(PAN);
    servoTilt.attach(TILT);
    centerFov(); 
}

/**
 * Updates pan and tilt with offset values
 * 
 * @param pan_sum pan offset
 * @param tilt_sum tilt offset
 */
void Pan_Tilt::updateServos(int8_t pan_sum, int8_t tilt_sum) {
    pan += pan_sum;
    tilt += tilt_sum;

    pan = constrain(pan, 0, 180);
    tilt = constrain(tilt, 0, 75);

    servoPan.write(pan);
    servoTilt.write(tilt);
}

/**
 * @return pan value
 */
int16_t Pan_Tilt::getPan() const {
    return pan;
}

/**
 * @return tilt value
 */
int16_t Pan_Tilt::getTilt() const {
    return tilt;
}