#ifndef STATO_MARCIA_H
#define STATO_MARCIA_H

#include "StatoRobot.h"

class StatoMarcia {
private:
    StatoRobot statoAttuale = IDLE;

    StatoMarcia();

    StatoMarcia(const StatoMarcia&) = delete;
    void operator=(const StatoMarcia&) = delete;

public:

    static StatoMarcia& getInstance();

    StatoRobot stato() const;
    void idle();
    void movimento();
    void torre();
};

#endif