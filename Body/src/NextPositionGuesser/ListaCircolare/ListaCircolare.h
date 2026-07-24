#ifndef LISTA_CIRCOLARE_H
#define LISTA_CIRCOLARE_H

#include <Arduino.h>

constexpr uint8_t LEN = 15;

/**
 * classe che implementa una lista circolare di interi di lunghezza LEN.
 */
struct ListaCircolare {
    private:
    int16_t entries[LEN] = {0};
    uint8_t next = 0;

    public:
    void add(int16_t entry);
    const int16_t* getEntries() const;
};

#endif // LISTA_CIRCOLARE_H
