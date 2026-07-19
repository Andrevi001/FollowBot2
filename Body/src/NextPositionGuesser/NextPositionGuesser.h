#include <Arduino.h>
#include "ListaCircolare/ListaCircolare.h"

struct NextPositionGuesser {
    private:
    ListaCircolare panValues;
    ListaCircolare tiltValues;
    ListaCircolare distanceValues;

    public:
    void addValues(int16_t pan, int16_t tilt, uint8_t distance) {
        panValues.add(pan);
        tiltValues.add(tilt);
        distanceValues.add(distance);
    }

    void guess(int16_t& predictedPan, int16_t& predictedTilt, int16_t& predictedDistance) {
        int16_t sumPan = 0;
        const int16_t* panVals = panValues.getEntries();
        for (uint8_t i = 0; i < len ; i++ ) {
            sumPan += panVals[i];
        }
        predictedPan = sumPan/len;

        int16_t sumTilt = 0;
        const int16_t* tiltVals = tiltValues.getEntries();
        for (uint8_t i = 0; i < len ; i++) {
            sumTilt += tiltVals[i];
        }
        predictedTilt = sumTilt/len;

        int16_t sumDis = 0;
        const int16_t* disVals = distanceValues.getEntries();
        for (uint8_t i = 0; i < len ; i++) {
            sumDis += disVals[i];
        }
        predictedDistance = sumDis/len;
    }
};