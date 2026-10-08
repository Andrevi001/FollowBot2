#include "CircularList.h"

/**
 * function to add elements to the list.
 * If the list is full, the first element of the list will be substituted, restaring the turn.
 * 
 * @param entry next element to add to the list
 */
void CircularList::add(int16_t entry) {
    entries[next] = entry;
    next++;
    if (next == LEN) {
        next = 0;
    }
}

/**
 * Used to obtain the elements of the list.
 * 
 * @return immutable array of elements
 */
const int16_t* CircularList::getEntries() const {
    return entries;
}