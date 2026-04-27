#include <motori.h>
#include <servo.h>

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);

    servoPan.attach(PAN);
    servoTilt.attach(TILT);
    pt.centerFov();

    //pin logica di controllo per le ruote
    pinMode(STBY, OUTPUT);
    pinMode(AIN1,OUTPUT);
    pinMode(AIN2,OUTPUT);
    pinMode(BIN1,OUTPUT);
    pinMode(BIN2,OUTPUT);

    //pin regolamento della velocità(PWM)
    ledcSetup(6, 20000, 8);
    ledcAttachPin(PWM, 6);
    ledcWrite(6, 40);

    //STBY sempre HIGH (non va mai in standby)
    digitalWrite(STBY, HIGH);

    Serial.println("Hello!");
}

void loop() {


    
    while (Serial2.available() >= 3) {
        dati.header = Serial2.read();
        dati.pan_next = Serial2.read();
        dati.tilt_next = Serial2.read();

        if (dati.header == 80) {
            pt.updateServos(dati.pan_next, dati.tilt_next);
        }
    }

    if (pt.getPan() >= 130 && dati.header == 80) {
        SxRotation();
        Serial.println("SX");
    } else if (pt.getPan() <= 40 && dati.header == 80) {
        DxRotation();
        Serial.println("DX");
    } else {
        Stop();
        Serial.println("SS");
    }
}