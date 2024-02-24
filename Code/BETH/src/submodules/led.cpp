#include "led.h"

#include <Adafruit_NeoPixel.h>
#include <Arduino.h>

#include "config.h"
#include "debug.h"

LEDs::LEDs(Adafruit_NeoPixel* ws2812b) {
    this->ws2812b = ws2812b;
    ws2812b->begin();
    ws2812b->clear();
}

LEDs::~LEDs() {
    ws2812b->clear();
    ws2812b->show();
    ws2812b->~Adafruit_NeoPixel();
    delete ws2812b;
}

void LEDs::setLED(unsigned int led, unsigned int r, unsigned int g, unsigned int b) {
    r = r > 255 ? 255 : r;
    g = g > 255 ? 255 : g;
    b = b > 255 ? 255 : b;
    ws2812b->setPixelColor(led, r, g, b);
    ws2812b->show();
}

void LEDs::setLED(unsigned int led, Color color) {
    color.r = color.r > 255 ? 255 : color.r;
    color.g = color.g > 255 ? 255 : color.g;
    color.b = color.b > 255 ? 255 : color.b;
    ws2812b->setPixelColor(led, color.r, color.g, color.b);
    ws2812b->show();
}

void LEDs::turnOffLED(unsigned int led) {
    ws2812b->setPixelColor(led, 0, 0, 0);
    ws2812b->show();
}

void LEDs::turnOffAllLEDs(bool statusLed) {
    for (int i = 0; i < LED_COUNT; i++) {
        if (statusLed && i == STATUS_LED) {
            continue;
        }
        ws2812b->setPixelColor(i, 0, 0, 0);
    }
    ws2812b->show();
}

void LEDs::turnOnAllLEDs() {
    for (int i = 0; i < LED_COUNT; i++) {
        if (i == STATUS_LED) {
            continue;
        }
        ws2812b->setPixelColor(i, 255, 255, 255);
    }
    ws2812b->show();
}

void LEDs::turnOnAllLEDs(Color color) {
    for (int i = 0; i < LED_COUNT; i++) {
        if (i == STATUS_LED) {
            continue;
        }
        ws2812b->setPixelColor(i, color.r, color.g, color.b);
    }
    ws2812b->show();
}

void LEDs::rainbow() {
    for (int i = 0; i < LED_COUNT; i++) {
        if (i == STATUS_LED) {
            continue;
        }
        ws2812b->setPixelColor(i, ws2812b->ColorHSV(rainbowIndex));
    }
    ws2812b->show();
    rainbowIndex += 256;
    if (rainbowIndex > 65535) {
        rainbowIndex = 0;
    }
}

void LEDs::heartbeat(Color color) {
    for (int i = 0; i < LED_COUNT; i++) {
        if (i == STATUS_LED) {
            continue;
        }
        ws2812b->setPixelColor(i, ws2812b->Color(color.r * heartbeatIndex / 255, color.g * heartbeatIndex / 255, color.b * heartbeatIndex / 255));
    }
    ws2812b->show();
    if (heartbeatDirection == 0) {
        heartbeatIndex += 5;
        if (heartbeatIndex > 255) {
            heartbeatIndex = 255;
            heartbeatDirection = 1;
        }
    } else {
        heartbeatIndex -= 5;
        if (heartbeatIndex < 0) {
            heartbeatIndex = 0;
            heartbeatDirection = 0;
        }
    }
}

std::string LEDs::addBlink(std::string name, Color color, int times, int ledIndex) {
    blinks.emplace(name, new Blink(color, times, ledIndex));
    return name;
}

bool LEDs::progressBlink(std::string name) {
    Blink* blink = blinks[name];
    blink->counter++;
    if (blink->counter > blink->times * 2) {
        if (blink->ledIndex != -1) {
            turnOffLED(blink->ledIndex);
        } else {
            turnOffAllLEDs();
        }
        blinks.erase(name);
        delete blink;
        return false;
    }

    if (blink->counter % 2 == 0) {
        if (blink->ledIndex != -1) {
            setLED(blink->ledIndex, blink->color);
        } else {
            for (int i = 0; i < LED_COUNT; i++) {
                if (i == STATUS_LED) {
                    continue;
                }
                setLED(i, blink->color);
            }
        }
    } else {
        if (blink->ledIndex != -1) {
            turnOffLED(blink->ledIndex);
        } else {
            turnOffAllLEDs();
        }
    }

    return true;
}