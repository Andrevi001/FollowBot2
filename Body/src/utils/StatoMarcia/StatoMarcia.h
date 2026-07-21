#ifndef STATO_MARCIA_H
#define STATO_MARCIA_H

class StatoMarcia {
private:
    bool inMovimento;
    StatoMarcia();

    StatoMarcia(const StatoMarcia&) = delete;
    void operator=(const StatoMarcia&) = delete;

public:
    static StatoMarcia& getInstance();

    bool isInMovimento() const;
    void impostaInMovimento();
    void resettaInMovimento();
};

#endif