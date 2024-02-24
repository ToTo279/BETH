#ifndef LED_H
#define LED_H

#include <Adafruit_NeoPixel.h>
#include <Arduino.h>

#include <unordered_map>
#include <vector>

#include "config.h"

using namespace std;

struct Color {
    unsigned int r = 0;
    unsigned int g = 0;
    unsigned int b = 0;
    Color(unsigned int r, unsigned int g, unsigned int b) : r(r), g(g), b(b) {}
};

struct Blink {
    Color color;
    int times;
    int ledIndex = -1;
    int counter = 0;
    Blink(Color color, int times, int ledIndex = -1) : color(color), times(times), ledIndex(ledIndex) {}
};

class LEDs {
   private:
    Adafruit_NeoPixel* ws2812b;
    uint16_t rainbowIndex = 0;
    int heartbeatIndex = 0;
    int heartbeatDirection = 0;
    std::unordered_map<std::string, Blink*> blinks;

   public:
    LEDs(Adafruit_NeoPixel* ws2812b);
    ~LEDs();
    void setLED(unsigned int led, unsigned int r, unsigned int g, unsigned int b);
    void setLED(unsigned int led, Color color);
    void turnOffLED(unsigned int led);
    void turnOffAllLEDs(bool statusLed = false);
    void turnOnAllLEDs();
    void turnOnAllLEDs(Color color);
    void rainbow();
    void heartbeat(Color color = {255, 0, 0});
    std::string addBlink(std::string name, Color color, int times, int ledIndex = -1);
    bool progressBlink(std::string name);
};

#endif