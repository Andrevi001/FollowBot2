#include <Arduino.h>
#include "utils.h"
#include "motori/motori.h"
#include "Pan_Tilt/Pan_Tilt.h"
#include "StatoMarcia/StatoMarcia.h"

datiUpdate dati;
Pan_Tilt& pt = Pan_Tilt::getInstance();
NextPositionGuesser guesser;
StatoMarcia& stato = StatoMarcia::getInstance();

bool avvicinamento = false;
bool allontanamento = false;
bool nuovoDato = false;

/** 
 * Funzione per la lettura dei dati inviati dal centro di elaborazione tramite Serial2. 
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
            dati.pan_next = (int8_t)panGuess;
            dati.tilt_next = (int8_t)tiltGuess;
            dati.distanza =(uint8_t)distanceGuess;
        }

        nuovoDato = true;
    }
}

/** 
 * Funzione per l'allineamento del corpo con la camera. 
 * Se viene superato il limSx il corpo gira a sinistra, se invece viene superato il limite destro il corpo gira a destra.
 */
void allineaCameraCorpo(uint8_t limSx, uint8_t limDx) {
    if (pt.getPan() > limSx && dati.header == 80) {
        SxRotation();
        Serial.println("SX");
    } else if (pt.getPan() < limDx && dati.header == 80) {
        DxRotation();
        Serial.println("DX");
    } else {
        Stop();
    }
}

/** 
 * Funzione per decidere il movimento in avvicinamento o allontanamento dal bersaglio.
 * Il movimento avviene lungo l'asse perpendicolare al bersaglio.
 * Si avvicina se la distanza è oltre i 160cm, si allontana se è sotto i 100cm e oltre i 20cm.
 */
void FwBw() {
    if (avvicinamento) {
        if (pt.getPan() > 90 || pt.getPan() < 80) {
            allineaCameraCorpo(90, 80);
            return;
        }
        Forward();
    } else if (allontanamento) {
        if (pt.getPan() > 100 || pt.getPan() < 70) {
            allineaCameraCorpo(100, 70);
            return;
        }
        Backward();
    }
}

/** 
 * Funzione che si occupa della gestione dello stato del robot.
 * Quindi il movimento pan/tilt, l'allineamento corpo/camera e la decisione di movimento in avvicinamento/allontanamento.
 */
void muoviCorpo() {

    if (nuovoDato) {
        pt.updateServos(dati.pan_next, dati.tilt_next);
        nuovoDato = false;
    }
    
    if (stato.stato() == TORRE) {
        allineaCameraCorpo(150,20);
    }

    if (avvicinamento || allontanamento) {
        FwBw();
        stato.movimento();
    } else if (stato.stato() == MOVIMENTO) {
        Stop();
        stato.torre();
    }
}