#include "StatoMarcia.h"

StatoMarcia::StatoMarcia() : inMovimento(false) {}

StatoMarcia& StatoMarcia::getInstance() {
    static StatoMarcia instance; 
    return instance;
}

bool StatoMarcia::isInMovimento() const {
    return inMovimento;
}

void StatoMarcia::impostaInMovimento() {
    inMovimento = true;
}

void StatoMarcia::resettaInMovimento() {
    inMovimento = false;
}