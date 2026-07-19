#include <Arduino.h>

constexpr uint8_t len = 10;

struct ListaCircolare {
    private:
    int16_t entries[len] = {0};
    uint8_t next = 0;

    public:
    void add(int16_t entry) {
        entries[next] = entry;
        next++;
        if (next == len) {
            next = 0;
        }
    }

    const int16_t* getEntries() const {
        return entries;
    }
};
