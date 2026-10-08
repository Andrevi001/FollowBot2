#ifndef CIRCULAR_LIST_H
#define CIRCULAR_LIST_H

#include <Arduino.h>

constexpr uint8_t LEN = 15;

/**
 * Class that implements a circular list of LEN integers.
 */
struct CircularList {
    private:
    int16_t entries[LEN] = {0};
    uint8_t next = 0;

    public:
    void add(int16_t entry);
    const int16_t* getEntries() const;
};

#endif
