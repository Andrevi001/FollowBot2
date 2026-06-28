#include <Arduino.h>

//Setup motori
// singolo standby
#define STBY 5

//singolo valore PWM
#define PWM 21

// canale A
#define AIN1 4 //marrone
#define AIN2 15 //viola

//canale B
#define BIN1 18 //grigio
#define BIN2 19 //bianco

void Forward() {
  //ruota destra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //ruota sinistra
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
}

void Backward() {
  //ruota sinistra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //ruota destra
  digitalWrite(BIN2, LOW);
  digitalWrite(BIN1, HIGH);
}

void DxRotation() {
  //ruota sinistra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  //ruota destra
  digitalWrite(BIN2, HIGH);
  digitalWrite(BIN1, LOW);
}

void SxRotation() {
  //ruota sinistra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  //ruota destra
  digitalWrite(BIN2, LOW);
  digitalWrite(BIN1, HIGH);
}

void Stop() {
  //ruota sinistra
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, HIGH);

  //ruota sinistra
  digitalWrite(BIN2, HIGH);
  digitalWrite(BIN1, HIGH);

  delay(100);

  //ruota anteriore sinistra
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);

  //ruota posteriore destra
  digitalWrite(BIN2, LOW);
  digitalWrite(BIN1, LOW);
}
