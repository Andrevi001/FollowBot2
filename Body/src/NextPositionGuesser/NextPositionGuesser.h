#ifndef NEXT_POSITION_GUESSER_H
#define NEXT_POSITION_GUESSER_H

#include <Arduino.h>
#include "ListaCircolare/ListaCircolare.h"

struct NextPositionGuesser {
    private:
    ListaCircolare panValues;
    ListaCircolare tiltValues;
    ListaCircolare distanceValues;

    int16_t mediaPonderata(const int16_t* valori);

    public:
    void addValues(int16_t pan, int16_t tilt, uint8_t distance);
    void guess(int16_t& predictedPan, int16_t& predictedTilt, int16_t& predictedDistance);
};

#endif // NEXT_POSITION_GUESSER_H