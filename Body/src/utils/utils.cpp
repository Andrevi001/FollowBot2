#include <Arduino.h>
#include "utils.h"
#include "motori/motori.h"
#include "servo/servo.h"

datiUpdate dati;
NextPositionGuesser guesser;
bool fwBw = false;

/** Funzione per la lettura dei dati inviati dal centro di elaborazione tramite la seriale 2. 
 * I dati vengono letti in blocchi di 4 byte e salvati nella struttura datiUpdate. 
 */
void leggiUpdate() {
    while (Serial2.available() >= 4) {
        dati.header = Serial2.read();
        dati.pan_next = Serial2.read();
        dati.tilt_next = Serial2.read();
        dati.distanza = Serial2.read();

        if (dati.header == 80) {
            guesser.addValues(dati.pan_next, dati.tilt_next, dati.distanza);
        } else {
            int16_t panGuess;
            int16_t tiltGuess;
            int16_t distanceGuess;
            guesser.guess(panGuess, tiltGuess, distanceGuess);
            dati.pan_next = panGuess;
            dati.tilt_next = tiltGuess;
            dati.distanza =(uint8_t)distanceGuess;
        }
    }
}

/** Funzione per l'allineamento del corpo con la camera. 
 * Se viene superato il limSx il corpo gira a sinistra, se invece viene superato il limite destro il corpo gira a destra.
 */
void allineaCameraCorpo(uint8_t limSx, uint8_t limDx) {
    if (pt.getPan() > limSx) {
        SxRotation();
    } else if (pt.getPan() < limDx) {
        DxRotation();
    } else if (!fwBw) {
        Stop();
    } else {
        fwBw = false;
    }
}

/** Funzione per decidere il movimento in avvicinamento o allontanamento dal bersaglio.
 * Il movimento avviene lungo l'asse perpendicolare al bersaglio.
 * Si avvicina se la distanza è oltre i 160cm, si allontana se è sotto i 100cm e oltre i 20cm.
 */
void FwBw() {
    bool avvicinamento = dati.distanza > 160;
    bool allontanamento = dati.distanza < 100 && dati.distanza > 20;

    if (avvicinamento || allontanamento) {

        if (pt.getPan() > 88 || pt.getPan() < 82) {
            allineaCameraCorpo(88, 82);
            return;
        }
        
        if (avvicinamento) {
            Forward();
        } else if (allontanamento) {
            Backward();
        } else {
            Stop();
            fwBw = false;
            return;
        }

        fwBw = true;
    }
}

/** Funzione che accorpa il movimento pan/tilt,
 * l'allineamento corpo/camera e la decisione di movimento in avvicinamento/allontanamento. */
void muoviCorpo() {
    pt.updateServos(dati.pan_next, dati.tilt_next);
    allineaCameraCorpo(150,20);
    FwBw();
}