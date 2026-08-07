#include <Arduino.h>
#include "utils/utils.h"
#include "Pan_Tilt/Pan_Tilt.h"
#include "motori/motori.h"

void setup() {
    //Comunicazione seriale
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);

    //inizializzo Pan_Tilt
    Pan_Tilt::getInstance().begin();

    //pin logica di controllo per le ruote
    pinMode(STBY, OUTPUT);
    pinMode(AIN1,OUTPUT);
    pinMode(AIN2,OUTPUT);
    pinMode(BIN1,OUTPUT);
    pinMode(BIN2,OUTPUT);

    //pin regolamento della velocità(PWM)
    ledcSetup(canale, 20000, 8);
    ledcAttachPin(PWM, canale);
    ledcWrite(canale, 50);

    //STBY sempre HIGH (non va mai in standby)
    digitalWrite(STBY, HIGH);

    //messaggio di avvio.
    Serial.println("Hello!");
}

void loop() {
    leggiUpdate();

    avvicinamento = dati.distanza > MaxDistanceCm;
    allontanamento = dati.distanza < MinDistanceCm && dati.distanza > 20;
    muoviCorpo();
}