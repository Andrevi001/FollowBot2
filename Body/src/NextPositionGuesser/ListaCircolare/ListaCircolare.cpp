#include "ListaCircolare.h"

void ListaCircolare::add(int16_t entry) {
    entries[next] = entry;
    next++;
    if (next == LEN) {
        next = 0;
    }
}

const int16_t* ListaCircolare::getEntries() const {
    return entries;
}