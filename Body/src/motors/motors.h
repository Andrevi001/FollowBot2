#ifndef MOTORS_H
#define MOTORS_H

#include <Arduino.h>

// Setup motors
// Single standby
constexpr uint8_t STBY = 5;

// singolo valore PWM
constexpr uint8_t PWM = 21;
constexpr uint8_t channel = 6;

// Motor A
constexpr uint8_t AIN1 = 4;  // brown
constexpr uint8_t AIN2 = 15; // purple

// Motor B
constexpr uint8_t BIN1 = 18; // grey
constexpr uint8_t BIN2 = 19; // white

// Functions 
void Forward();
void Backward();
void DxRotation();
void SxRotation();
void Stop();

#endif
