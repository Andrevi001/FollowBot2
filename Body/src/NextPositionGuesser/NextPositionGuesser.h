#ifndef NEXT_POSITION_GUESSER_H
#define NEXT_POSITION_GUESSER_H

#include <Arduino.h>
#include "CircularList/CircularList.h"

/**
 * Class built to guess the next position of the target based on previous positions.
 */
struct NextPositionGuesser {
    private:
    CircularList panValues;
    CircularList tiltValues;
    CircularList distanceValues;

    int16_t weightedAverage(const int16_t* valori);

    public:
    void addValues(int16_t pan, int16_t tilt, uint8_t distance);
    void guess(int16_t& predictedPan, int16_t& predictedTilt, int16_t& predictedDistance);
};

#endif