/**
 * Enum that defines the possible states of FollowBot2:
 *  -IDLE: idle state, FollowBot2 is stationary.
 *  -TOWER: Turret state; the robot's movement is limited to rotating clockwise/counterclockwise to keep the target in frame. 
 *  -ROVER: Approaching/receding state; the robot centers the target in the frame and then moves closer or further away based on distance. 
 */
enum RobotState {
    IDLE,
    TOWER,
    ROVER
};