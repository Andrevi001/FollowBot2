#include <Arduino.h>
#include "ListaCircolare/ListaCircolare.h"

struct NextPositionGuesser {
    private:
    ListaCircolare panValues;
    ListaCircolare tiltValues;
    ListaCircolare distanceValues;

    int16_t mediaPonderata(const int16_t* valori) {
        int32_t sommaPonderata = 0;
        uint16_t sommaPesi = 0;

        for (uint8_t i = 0; i < LEN; i++) {
            uint8_t peso = i + 1;
            sommaPonderata += valori[i] * peso;
            sommaPesi += peso;
        }

        return (int16_t)(sommaPonderata / sommaPesi);
    }

    public:
    void addValues(int16_t pan, int16_t tilt, uint8_t distance) {
        panValues.add(pan);
        tiltValues.add(tilt);
        distanceValues.add(distance);
    }

    void guess(int16_t& predictedPan, int16_t& predictedTilt, int16_t& predictedDistance) {
        predictedPan = mediaPonderata(panValues.getEntries());
        predictedTilt = mediaPonderata(tiltValues.getEntries());
        predictedDistance = mediaPonderata(distanceValues.getEntries());
    }
};