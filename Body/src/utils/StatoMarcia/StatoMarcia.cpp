#include "StatoMarcia.h"

/**
 * funzione per ottenere l'unica istanza della classe.
 */
StatoMarcia& StatoMarcia::getInstance() {
    static StatoMarcia instance; 
    return instance;
}

/**
 * funzione per ottenere lo stato attuale.
 */
StatoRobot StatoMarcia::stato() {
    return statoAttuale;
}

/**
 * Cambio stato in IDLE
 */
void StatoMarcia::idle() {
    statoAttuale = IDLE;
}

/**
 * Cambio stato in TORRE
 */
void StatoMarcia::torre() {
    statoAttuale = TORRE;
}

/**
 * Cambio stato in MOVIMENTO
 */
void StatoMarcia::movimento() {
    statoAttuale = MOVIMENTO;
}