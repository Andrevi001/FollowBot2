#include <comunicazioni.h>

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);
    busEsp.begin(Serial2);
    Serial.println("Hello!");
}

void loop() {
    busEsp.tick();

    if (busEsp.available()) {
        busEsp.rxObj(dati);
        Serial.printf("header: %c\n",dati.header);
    }
}