#include "MotionState.h"

/**
 * Used to obtain the sigleton instance.
 * 
 * @return singleton instance
 */
MotionState& MotionState::getInstance() {
    static MotionState instance; 
    return instance;
}

/**
 * Used to obtain the current motion state.
 * 
 * @return current state
 */
RobotState MotionState::state() {
    return currentState;
}

/**
 * Changes the state to RobotState.IDLE
 */
void MotionState::idle() {
    currentState = IDLE;
}

/**
 * Chages the state to RobotState.TOWER
 */
void MotionState::tower() {
    currentState = TOWER;
}

/**
 * Changes the state to RobotState.ROVER
 */
void MotionState::rover() {
    currentState = ROVER;
}