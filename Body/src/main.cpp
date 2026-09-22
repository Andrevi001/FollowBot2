#include <Arduino.h>
#include "utils/utils.h"
#include "Pan_Tilt/Pan_Tilt.h"
#include "motors/motors.h"

void setup() {
    //Serial communication
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);

    //initializing Pan_Tilt
    Pan_Tilt::getInstance().begin();

    //initializing wheel control pins
    pinMode(STBY, OUTPUT);
    pinMode(AIN1,OUTPUT);
    pinMode(AIN2,OUTPUT);
    pinMode(BIN1,OUTPUT);
    pinMode(BIN2,OUTPUT);

    //Speed controll pin(PWM)
    ledcSetup(channel, 20000, 8);
    ledcAttachPin(PWM, channel);
    ledcWrite(channel, 50);

    //STBY always HIGH
    digitalWrite(STBY, HIGH);

    //Starting message.
    Serial.println("Hello!");
}

void loop() {
    readUpdate();

    approach = data.distance > MaxDistanceCm;
    recede = data.distance < MinDistanceCm && data.distance > 20;
    react();
}