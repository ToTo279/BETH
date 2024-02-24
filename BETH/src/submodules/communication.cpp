#include <Arduino.h>
#include <WiFi.h>
#include "communication.h"

#include "config.h"
#include "debug.h"

Connection::Connection() {
    WiFi.mode(WIFI_STA);
    // this->tcpClient = client;
}

Connection::~Connection() {
    // tcpClient->stop();
}

void Connection::connectWiFi() {
    DEBUG_PRINT("Connecting to WiFi ..");
    WiFi.begin(BASE_STATION_SSID, BASE_STATION_PSA2_PSK);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        DEBUG_PRINT(".");
        if (WiFi.status() == WL_CONNECT_FAILED) {
            WiFi.disconnect();
            WiFi.begin(BASE_STATION_SSID, BASE_STATION_PSA2_PSK);
        }
        delay(500);
    }

    DEBUG_PRINTLN("");
    DEBUG_PRINT("Connected to ");
    DEBUG_PRINTLN(WiFi.SSID());
    DEBUG_PRINT("IP Address: ");
    DEBUG_PRINTLN(WiFi.localIP());
    DEBUG_PRINT("Gateway Address: ");
    DEBUG_PRINTLN(WiFi.gatewayIP());

    // String ip = wifi->gatewayIP().toString();
    // char* charBuf = new char[ip.length() + 1];
    // strcpy(charBuf, ip.c_str());
    // hostIP = charBuf;

    // DEBUG_PRINT("Host IP: ");
    // DEBUG_PRINTLN(hostIP);
}

void Connection::connectTCP() {
    DEBUG_PRINT("Connecting to TCP Server ");
    DEBUG_PRINT(hostIP);
    DEBUG_PRINT(":");
    DEBUG_PRINT(TCP_PORT);
    DEBUG_PRINT(" ..");

    // tcpClient->connect(hostIP, TCP_PORT);
    // while (!tcpClient->connect(hostIP, TCP_PORT)) {
    //     if (!tcpClient->connected()) {
    //         DEBUG_PRINT('.');
    //         delay(100);
    //     }
    // }
    DEBUG_PRINTLN("");
    DEBUG_PRINTLN("Connected to TCP Server");
}

void Connection::handShake() {
    // doc["id"] = SATELLITE_ID;
    // doc["battery_status"] = battery_percentage;
    // char buffer[256];
    // serializeJson(doc, buffer);
    // tcpClient->println(buffer);
    // DEBUG_PRINT("Handshake sent with ID:");
    // DEBUG_PRINTLN(SATELLITE_ID);
}

bool Connection::sendMessage(String message) {
    // if (tcpClient->connected()) {
    //     return false;
    // }

    // doc["message"] = message;
    // serializeJson(doc, tcpClient);
    // return true;
}

DynamicJsonDocument Connection::receiveMessage() {
    // DynamicJsonDocument doc(jsonCapacity);
    // deserializeJson(doc, tcpClient);
    // return doc;
}

bool Connection::setBatteryStatus(unsigned int percentage) {
    battery_percentage = percentage;
    return true;
}