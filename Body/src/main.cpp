#include <Arduino.h>
#include <servo.h>

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);

    servoPan.attach(PAN);
    servoTilt.attach(TILT);
    pt.centerFov();

    Serial.println("Hello!");
}

void loop() {
    if (Serial2.available() >= 3) {
        uint8_t header = Serial2.read();
        int8_t pan_next = Serial2.read();
        int8_t tilt_next = Serial2.read();
        
        if (header == 80) {
            pt.updateServos(pan_next, tilt_next);
        }
    }
}