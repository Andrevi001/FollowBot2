#include <Arduino.h>
#include "NextPositionGuesser/NextPositionGuesser.h"

struct datiUpdate {
    uint8_t header;
    int8_t pan_next;
    int8_t tilt_next;
    uint8_t distanza;
}dati;

NextPositionGuesser guesser;