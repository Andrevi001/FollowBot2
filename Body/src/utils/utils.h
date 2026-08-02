#ifndef UTILS_H
#define UTILS_H

#include <Arduino.h>
#include "NextPositionGuesser/NextPositionGuesser.h"

/**
 * Insieme di funzioni e variabili globali.
 */

struct datiUpdate {
    uint8_t header;
    int8_t pan_next;
    int8_t tilt_next;
    uint8_t distanza;
};

extern datiUpdate dati;
extern NextPositionGuesser guesser;
extern bool avvicinamento;
extern bool allontanamento;
extern bool nuovoDato;
const uint8_t MaxDistanceCm = 160;
const uint8_t MinDistanceCm = 100;


void leggiUpdate();
void allineaCameraCorpo(uint8_t limSx, uint8_t limDx);
void FwBw();
void muoviCorpo();

#endif