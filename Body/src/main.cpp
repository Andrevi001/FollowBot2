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
    ledcSetup(canale, 20000, 8);
    ledcAttachPin(PWM, canale);

    //STBY sempre HIGH (non va mai in standby)
    digitalWrite(STBY, HIGH);

    Serial.println("Hello!");
}

void loop() {
    leggiUpdate();
    muoviCorpo();
}

/** Funzione per la lettura dei dati inviati dal centro di elaborazione tramite la seriale 2. 
 * I dati vengono letti in blocchi di 4 byte e salvati nella struttura datiUpdate. 
 * Se l'header è corretto (80), viene aggiornato il pan e tilt della telecamera. 
 */
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

/** Funzione per l'allineamento del corpo con la camera. 
 * Se viene superato il limSx il corpo gira a sinistra, se invece viene superato il limite destro il corpo gira a destra.
 */
void allineaCameraCorpo(uint8_t limSx, uint8_t limDx) {
    ledcWrite(canale, 50);
    if (pt.getPan() > limSx && dati.header == 80) {
        SxRotation();
    } else if (pt.getPan() < limDx && dati.header == 80) {
        DxRotation();
    } else {
        Stop();
    }
}

/** Funzione che accorpa l'allineamento corpo/camera e la decisione di movimento in avvicinamento/allontanamento. */
void muoviCorpo() {
    allineaCameraCorpo(150,20);
    FwBw();
}

/** Funzione per decidere il movimento in avvicinamento o allontanamento dal bersaglio.
 * Il movimento avviene lungo l'asse perpendicolare al bersaglio.
 * Si avvicina se la distanza è oltre i 160cm, si allontana se è sotto i 100cm e oltre i 20cm.
 */
void FwBw() {
    while(dati.distanza > 160 || (dati.distanza < 100 && dati.distanza > 20)) {
        leggiUpdate();
        if (pt.getPan() > 88 || pt.getPan() < 82) {
            allineaCameraCorpo(88, 82);
        }
        
        ledcWrite(canale, 100);
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