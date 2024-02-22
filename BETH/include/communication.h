#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <Arduino.h>
#include <WiFi.h>
#include "ArduinoJson.h"

class Connection {
    private:
        const size_t jsonCapacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;
        // WiFiClass* wifi;
        // WiFiClient* tcpClient;
        // DynamicJsonDocument doc;
        const char* hostIP;
        void handShake();
        unsigned int battery_percentage = 0;


    public:
        Connection();
        ~Connection();
        void connectWiFi();
        void connectTCP();
        bool sendMessage(String message);
        DynamicJsonDocument receiveMessage();
        bool setBatteryStatus(unsigned int percentage);
};

#endif