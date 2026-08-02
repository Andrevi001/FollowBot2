#ifndef MOTORI_H
#define MOTORI_H

#include <Arduino.h>

// Setup motori
// singolo standby
constexpr uint8_t STBY = 5;

// singolo valore PWM
constexpr uint8_t PWM = 21;
constexpr uint8_t canale = 6;

// canale A
constexpr uint8_t AIN1 = 4;  // marrone
constexpr uint8_t AIN2 = 15; // viola

// canale B
constexpr uint8_t BIN1 = 18; // grigio
constexpr uint8_t BIN2 = 19; // bianco

// Dichiarazioni delle funzioni 
void Forward();
void Backward();
void DxRotation();
void SxRotation();
void Stop();

#endif
