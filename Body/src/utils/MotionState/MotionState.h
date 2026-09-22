#ifndef MOTION_STATE_H
#define MOTION_STATE_H

#include "RobotState.h"

/**
 * Singleton class designed to manage the motion state of FollowBot2. Employs Enum RobotState.
 */
class MotionState {
private:
    RobotState currentState = TOWER;

    MotionState() = default;

    MotionState(const MotionState&) = delete;
    void operator=(const MotionState&) = delete;

public:

    static MotionState& getInstance();

    RobotState state();
    void idle();
    void tower();
    void rover();
};

#endif