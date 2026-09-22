#include "NextPositionGuesser.h"

/**
 * Function to calculate the weighted average of the given set of values
 * 
 * @param values set on which to calculate the weighted average
 * @return weighted average
*/
int16_t NextPositionGuesser::weightedAverage(const int16_t* values) {
    int32_t weightedSum = 0;
    uint16_t weightsSum = 0;

    for (uint8_t i = 0; i < LEN; i++) {
        uint8_t weight = i + 1;
        weightedSum += values[i] * weight;
        weightsSum += weight;
    }

    return (int16_t)(weightedSum / weightsSum);
}

/**
 * Function to add position values.
 * 
 * @param pan value
 * @param tilt value
 * @param distance value
 */
void NextPositionGuesser::addValues(int16_t pan, int16_t tilt, uint8_t distance) {
    panValues.add(pan);
    tiltValues.add(tilt);
    distanceValues.add(distance);
}

/**
 * Function used to predict the next position.
 * 
 * @param predictedPan pointer to the predicted value of the next pan offset
 * @param predictedTilt pointer to the predicted value of the next tilt offset
 * @param predictedDistance pointer to the predicted value of the next distance
 */
void NextPositionGuesser::guess(int16_t& predictedPan, int16_t& predictedTilt, int16_t& predictedDistance) {
    predictedPan = weightedAverage(panValues.getEntries());
    predictedTilt = weightedAverage(tiltValues.getEntries());
    predictedDistance = weightedAverage(distanceValues.getEntries());
}