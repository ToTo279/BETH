#ifndef DEBUG_H
#define DEBUG_H

#include <Arduino.h>
#include "config.h"



#ifdef DEBUG
    #define START_DEBUG Serial.begin(115200)
    #define DEBUG_PRINTLN(x) Serial.println(x)
    #define DEBUG_PRINT(x) Serial.print(x)
#else
    #define START_DEBUG
    #define DEBUG_PRINTLN(x)
    #define DEBUG_PRINT(x)
#endif

#endif