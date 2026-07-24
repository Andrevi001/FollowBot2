#include "ListaCircolare.h"

/**
 * funzione per aggiungere un nuovo elemento in lista.
 * Se la lista è piene si sostituisce il primo elemento del cerchio.
 */
void ListaCircolare::add(int16_t entry) {
    entries[next] = entry;
    next++;
    if (next == LEN) {
        next = 0;
    }
}

/**
 * Funzione per ottenere i dati in lista.
 */
const int16_t* ListaCircolare::getEntries() const {
    return entries;
}