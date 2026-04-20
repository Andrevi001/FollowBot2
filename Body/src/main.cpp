#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);
    Serial.println("Hello!");
}

void loop() {
    if (Serial2.available() >= 3) {
        uint8_t header = Serial2.read();
        int8_t pan = Serial2.read();
        int8_t tilt = Serial2.read();
        
        if (header == 80) {
            Serial.printf("H: %c, pan: %d, tilt: %d \n", header, pan, tilt);
        }
    }
}