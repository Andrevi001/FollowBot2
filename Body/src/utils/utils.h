#ifndef UTILS_H
#define UTILS_H

#include <Arduino.h>
#include "NextPositionGuesser/NextPositionGuesser.h"

/**
 * Utility class that also defines updateData structure
 */

struct updateData {
    uint8_t header;
    int8_t pan_next;
    int8_t tilt_next;
    uint8_t distance;
};

extern updateData data;
extern NextPositionGuesser guesser;
extern bool approach;
extern bool recede;
extern bool newData;
const uint8_t MaxDistanceCm = 160;
const uint8_t MinDistanceCm = 100;


void readUpdate();
void alignCameraAndBody(uint8_t limSx, uint8_t limDx);
void FwBw();
void react();

#endif