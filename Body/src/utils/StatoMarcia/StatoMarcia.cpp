#include "StatoMarcia.h"

StatoMarcia& StatoMarcia::getInstance() {
    static StatoMarcia instance; 
    return instance;
}

void StatoMarcia::idle() {
    statoAttuale = IDLE;
}

void StatoMarcia::torre() {
    statoAttuale = TORRE;
}

void StatoMarcia::movimento() {
    statoAttuale = MOVIMENTO;
}