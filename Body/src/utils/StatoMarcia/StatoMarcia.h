#ifndef STATO_MARCIA_H
#define STATO_MARCIA_H

#include "StatoRobot.h"

/**
 * Classe singleton che serve a gestire lo stato di FollowBot2. Utilizza Enum StatoRobot.
 */
class StatoMarcia {
private:
    StatoRobot statoAttuale = TORRE;

    StatoMarcia() = default;

    StatoMarcia(const StatoMarcia&) = delete;
    void operator=(const StatoMarcia&) = delete;

public:

    static StatoMarcia& getInstance();

    StatoRobot stato();
    void idle();
    void movimento();
    void torre();
};

#endif