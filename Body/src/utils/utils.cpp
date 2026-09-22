#include <Arduino.h>
#include "utils.h"
#include "motors/motors.h"
#include "Pan_Tilt/Pan_Tilt.h"
#include "MotionState/MotionState.h"

updateData data;
Pan_Tilt& pt = Pan_Tilt::getInstance();
NextPositionGuesser guesser;
MotionState& state = MotionState::getInstance();

bool approach = false;
bool recede = false;
bool newData = false;

/** 
 * Used to read the data sent by the center of processing through Serial2.
 * The data is read in blocks of 4 bytes, to be then saved in the updateData structure. 
 */
void readUpdate() {
    while (Serial2.available() >= 4) {
        data.header = Serial2.read();
        data.pan_next = Serial2.read();
        data.tilt_next = Serial2.read();
        data.distance = Serial2.read();

        if (data.header == 80) {
            guesser.addValues(data.pan_next, data.tilt_next, data.distance);
        } else {
            int16_t panGuess;
            int16_t tiltGuess;
            int16_t distanceGuess;
            guesser.guess(panGuess, tiltGuess, distanceGuess);
            data.pan_next = (int8_t)panGuess;
            data.tilt_next = (int8_t)tiltGuess;
            data.distance =(uint8_t)distanceGuess;
        }

        newData = true;
    }
}

/** 
 * used to align the rover's body and camera. 
 * if limSx is exceeded the body will turn counterclockwise, 
 * if limDx is exceeded the body will turn clockwise.
 * 
 * @param limSx left side limit for the value of pan
 * @param limDx right side limit for the value of pan 
 */
void alignCameraAndBody(uint8_t limSx, uint8_t limDx) {
    if (pt.getPan() > limSx && data.header == 80) {
        SxRotation();
    } else if (pt.getPan() < limDx && data.header == 80) {
        DxRotation();
    } else {
        Stop();
    }
}

/** 
 * Used to decide if to approach or recede from the target.
 * The movement is perpendicular to the target.
 * The rover will approach if the distance is over 160cm, it will recede if the distance is between 20cm and 100cm.
 */
void FwBw() {
    if (approach) {
        if (pt.getPan() > 90 || pt.getPan() < 80) {
            alignCameraAndBody(90, 80);
            return;
        }
        Forward();
    } else if (recede) {
        if (pt.getPan() > 100 || pt.getPan() < 70) {
            alignCameraAndBody(100, 70);
            return;
        }
        Backward();
    }
}

/** 
 * Used to coordinate the rover's movements (Pan/Tilt and wheels) using MotionState.
 */
void react() {

    if (newData) {
        pt.updateServos(data.pan_next, data.tilt_next);
        newData = false;
    }
    
    if (state.state() == TOWER) {
        alignCameraAndBody(150,20);
    }

    if (approach || recede) {
        FwBw();
        state.rover();
    } else if (state.state() == ROVER) {
        Stop();
        state.tower();
    }
}