#include <motori.h>
#include <servo.h>

struct datiUpdate {
    uint8_t header;
    int8_t pan_next;
    int8_t tilt_next;
    uint8_t distanza;
}dati;

void leggiUpdate();
void muoviCorpo();
void allineaCameraCorpo(uint8_t limSx, uint8_t limDx);
void FwBw();

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

    //STBY sempre HIGH (non va mai in standby)
    digitalWrite(STBY, HIGH);

    Serial.println("Hello!");
}

void loop() {
    
    leggiUpdate();
    muoviCorpo();
}

void leggiUpdate() {
    while (Serial2.available() >= 4) {
        dati.header = Serial2.read();
        dati.pan_next = Serial2.read();
        dati.tilt_next = Serial2.read();
        dati.distanza = Serial2.read();

        if (dati.header == 80) {
            pt.updateServos(dati.pan_next, dati.tilt_next);
        }
    }
}

void allineaCameraCorpo(uint8_t limSx, uint8_t limDx) {
    ledcWrite(6, 50);
    if (pt.getPan() > limSx && dati.header == 80) {
        SxRotation();
    } else if (pt.getPan() < limDx && dati.header == 80) {
        DxRotation();
    } else {
        Stop();
    }
}

void muoviCorpo() {
    allineaCameraCorpo(150,20);
    FwBw();
}

void FwBw() {
    while(dati.distanza > 160 || (dati.distanza < 100 && dati.distanza > 20)) {
        leggiUpdate();
        if (pt.getPan() > 88 || pt.getPan() < 82) {
            allineaCameraCorpo(88, 82);
        }
        
        ledcWrite(6, 100);
        if (dati.distanza > 160) {
            Forward();
        } else if (dati.distanza < 100 && dati.distanza > 20) {
            Backward();
        } else {
            Stop();
            return;
        }
    }
}