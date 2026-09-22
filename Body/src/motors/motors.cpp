#include <Arduino.h>
#include "motors.h"

void Forward() {
  //Right wheel
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //Left wheel
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
}

void Backward() {
  //Left wheel
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //Right wheel
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
}

void DxRotation() {
  //Left wheel
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //Right wheel
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
}

void SxRotation() {
  //Left wheel
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //Right wheel
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
}

void Stop() {
  //Left wheel
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, HIGH);

  //Right wheel
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, HIGH);

  delay(100);

  //Left wheel
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);

  //Right wheel
  digitalWrite(BIN2, LOW);
  digitalWrite(BIN1, LOW);
}