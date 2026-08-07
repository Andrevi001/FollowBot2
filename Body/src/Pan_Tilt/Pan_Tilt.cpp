#include "Pan_Tilt.h"

Pan_Tilt::Pan_Tilt() {}

/**
 * Funzione per centrare i servo. 
 */
void Pan_Tilt::centerFov() {
    pan = 85;
    tilt = 30;
    servoPan.write(pan);
    servoTilt.write(tilt);
}

/**
 * funzione per inizializzare i pin.
 */
void Pan_Tilt::begin() {
    servoPan.attach(PAN);
    servoTilt.attach(TILT);
    centerFov(); 
}

/**
 * funzione per aggiornare i servo
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
 * funzione per ottenere lo stato attuale del PAN
 */
int16_t Pan_Tilt::getPan() const {
    return pan;
}

/**
 * funzione per ottenere lo stato attuale del TILT
 */
int16_t Pan_Tilt::getTilt() const {
    return tilt;
}