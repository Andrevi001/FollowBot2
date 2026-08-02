#include <Arduino.h>
#include "motori.h"

void Forward() {
  //ruota destra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //ruota sinistra
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
}

void Backward() {
  //ruota sinistra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //ruota destra
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
}

void DxRotation() {
  //ruota sinistra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //ruota destra
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
}

void SxRotation() {
  //ruota sinistra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //ruota destra
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
}

void Stop() {
  //ruota sinistra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, HIGH);

  //ruota sinistra
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, HIGH);

  delay(100);

  //ruota anteriore sinistra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);

  //ruota posteriore destra
  digitalWrite(BIN2, LOW);
  digitalWrite(BIN1, LOW);
}