#include <Arduino.h>
#include "power.h"
#include "config.h"
#include "debug.h"

Power::Power(){
    DEBUG_PRINTLN("[Power] Initializing Power");
    pinMode(POWER_OFF_PIN, OUTPUT);
}

void Power::powerOff(){
    DEBUG_PRINTLN("[Power] Powering off");
    digitalWrite(POWER_OFF_PIN, HIGH);
}

unsigned int Power::getChargeStatus(){
    DEBUG_PRINTLN("[Power] Getting charge status");
    float value = analogRead(BATTERY_READ_PIN);
    value = static_cast<float>(value) - offset;
    value = value/(maximum-offset);
    value = value > 1 ? 1 : value;
    value = value < 0 ? 0 : value;
    return (unsigned int)value * 100;
}