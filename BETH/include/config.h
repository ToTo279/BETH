#ifndef CONFIG_H
#define CONFIG_H

#define DEBUG 1

// Network Configuration
#define SATELLITE_ID 0 // change this
#define HOST_IP "192.168.178.42"
#define TCP_PORT 8888
#define BASE_STATION_SSID "basepi"
#define BASE_STATION_PSA2_PSK "rasbase331"

// PINS
#define POWER_OFF_PIN 19
#define BATTERY_READ_PIN 34
#define LED_WS2812B_PIN 18  // The ESP32 pin GPIO16 connected to WS2812B
#define MP3_TX_PIN 17 // Connects to module's RX
#define MP3_RX_PIN 16 // Connects to module's TX
#define BUILLTIN_LED 2
#define VL53LOX_INTERRUPT_PIN_1 36
#define VL53LOX_INTERRUPT_PIN_2 35
#define VL53LOX_INTERRUPT_PIN_3 32
#define VL53LOX_OFFSET 65536.0

// Device Configuration
#define LED_COUNT 35   // The number of LEDs (pixels) on WS2812B LED strip
#define STATUS_LED 16   // The pin number of the status LED

#define BATTERY_UPDATE_INTERVAL 2 * 60 * 1000 // 2 minutes
#define BATTERY_MIDDLE_THRESHOLD 50
#define BATTERY_LOW_THRESHOLD 15


// Sound Configuration
#define STARTUP_SOUND 1
#define COUNTDOWN_SOUND 2
#define SWING_FAIL_SOUND 3
#define SWING_SUCCESS_SOUND 4


// Game Configuration
#define GAME_SWING_TIMEOUT 10 * 1000 // 20 seconds
#define GAME_SWING_DISTANCE_MAX 100 // in mm (20cm)
#define GAME_SWING_DISTANCE_MIN 50 // in mm (10cm)
#define GAME_SWING_DISTANCE_THRESHOLD 100 // in mm (100mm)



#endif