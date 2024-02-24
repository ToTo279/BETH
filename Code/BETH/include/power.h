#ifndef POWER_H
#define POWER_H

#include <Arduino.h>
#include "config.h"

class Power{
    private:
        const float offset = 1560.0f;
        const float maximum = 2440.0f;

    public:
        Power();
        ~Power();
        void powerOff();
        unsigned int getChargeStatus();

};

#endif