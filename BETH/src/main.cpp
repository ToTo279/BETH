#include <Adafruit_NeoPixel.h>
#include <Adafruit_VL53L0X.h>
#include <Arduino.h>
#include <DFPlayerMini_Fast.h>
#include <ReactESP.h>
#include <SoftwareSerial.h>
#include <WiFi.h>

using namespace reactesp;
using namespace dfplayer;

ReactESP app;

#include "audio.h"
// #include "communication.h"
#include "config.h"
#include "debug.h"
#include "led.h"
#include "power.h"
#include "sensor.h"

SoftwareSerial softwareSerial(MP3_RX_PIN, MP3_TX_PIN);
DFPlayerMini_Fast player;

Adafruit_NeoPixel ws2812b(LED_COUNT, LED_WS2812B_PIN, NEO_GRB + NEO_KHZ800);
WiFiClient tcpClient;

Adafruit_VL53L0X TOFsensor;

Audio* audio;
Power* power;
Sensor* sensor;
LEDs* leds;
// Connection* connection;

// Reactions
RepeatReaction* rainbowReaction;
RepeatReaction* heartbeatReaction;
RepeatReaction* sensorMeasurementReaction;

RepeatReaction* batteryIndicatorReaction;
int batteryIndicator = 0;
int batteryCurrentThreshold = 0;

RepeatReaction* connectedToBaseStationReaction;

DelayReaction* gameSwingTimeoutReaction;

void enterDebugMode();
void enterOperationMode();

///////////////////////////
//      OPERATION MODE
///////////////////////////

void enterOperationMode() {
    DEBUG_PRINTLN("Entering operation mode");
}

void connectToBaseStation() {
    DEBUG_PRINTLN("Connecting to base station");

    heartbeatReaction = app.onRepeat(15, []() {
        leds->heartbeat({0, 0, 255});
    });
    // TODO: Implement connection to base station

    app.onDelay(5000, []() {
        app.remove(heartbeatReaction);
        leds->turnOffAllLEDs();
        std::string blinkName = leds->addBlink("connectedToBaseStation", {0, 255, 0}, 7, -1);
        connectedToBaseStationReaction = app.onRepeat(50, [blinkName]() {
            if (!leds->progressBlink(blinkName)) {
                app.remove(connectedToBaseStationReaction);
            }
        });
    });
}

void indicateBatteryLevel(int batteryLevel) {
    Color color = {0, 255, 0};
    color = batteryLevel < BATTERY_MIDDLE_THRESHOLD ? Color(200, 80, 0) : color;  // yellow 200, 80, 0
    color = batteryLevel < BATTERY_LOW_THRESHOLD ? Color(255, 0, 0) : color;

    std::string blinkName = leds->addBlink("batteryIndicator", color, 5, STATUS_LED);

    batteryIndicatorReaction = app.onRepeat(150, [blinkName]() {
        if (!leds->progressBlink(blinkName)) {
            app.remove(batteryIndicatorReaction);
        }
    });
}

void registerBatteryUpdateTask() {
    app.onRepeat(BATTERY_UPDATE_INTERVAL, []() {
        int batteryLevel = power->getChargeStatus();
        if (batteryLevel < BATTERY_MIDDLE_THRESHOLD && batteryCurrentThreshold == 100) {
            batteryCurrentThreshold = BATTERY_MIDDLE_THRESHOLD;
            indicateBatteryLevel(batteryLevel);
        } else if (batteryLevel < BATTERY_LOW_THRESHOLD && batteryCurrentThreshold == BATTERY_MIDDLE_THRESHOLD) {
            batteryCurrentThreshold = BATTERY_LOW_THRESHOLD;
            indicateBatteryLevel(batteryLevel);
        }else if(batteryLevel > batteryCurrentThreshold && batteryCurrentThreshold == BATTERY_LOW_THRESHOLD){
            batteryCurrentThreshold = BATTERY_MIDDLE_THRESHOLD;
            indicateBatteryLevel(batteryLevel);
        }else if(batteryLevel > batteryCurrentThreshold && batteryCurrentThreshold == BATTERY_MIDDLE_THRESHOLD){
            batteryCurrentThreshold = 100;
            indicateBatteryLevel(batteryLevel);
        }
    });
}

void setupBattery() {
    int batteryLevel = power->getChargeStatus();
    batteryCurrentThreshold = 100;
    batteryCurrentThreshold = batteryLevel < BATTERY_MIDDLE_THRESHOLD ? BATTERY_MIDDLE_THRESHOLD : batteryCurrentThreshold;
    batteryCurrentThreshold = batteryLevel < BATTERY_LOW_THRESHOLD ? BATTERY_LOW_THRESHOLD : batteryCurrentThreshold;
    batteryIndicator = 0;
    indicateBatteryLevel(batteryLevel);
    registerBatteryUpdateTask();
}

///////////////////////////
//   GAME LOGIC
///////////////////////////
void waitForSwing();

void swingSuccess() {
    DEBUG_PRINTLN("SUCCESS: Swing detected");
    app.remove(sensorMeasurementReaction);
    app.remove(gameSwingTimeoutReaction);
    sensor->stopMeasurement();
    leds->turnOffAllLEDs();
    audio->play(SWING_SUCCESS_SOUND);
    leds->turnOnAllLEDs({0, 255, 0});
    app.onDelay(1000, []() {
        leds->turnOffAllLEDs();
        app.onDelay(1000, []() {
            waitForSwing();
        });
    });
}

void swingFailure() {
    DEBUG_PRINTLN("FAILURE: Swing not detected");
    app.remove(sensorMeasurementReaction);
    app.remove(gameSwingTimeoutReaction);
    sensor->stopMeasurement();
    leds->turnOffAllLEDs();
    audio->play(SWING_FAIL_SOUND);
    leds->turnOnAllLEDs({255, 0, 0});
    app.onDelay(1000, []() {
        leds->turnOffAllLEDs();
        app.onDelay(1000, []() {
            waitForSwing();
        });
    });
}

void waitForSwing() {
    DEBUG_PRINTLN("Waiting for swing");
    leds->turnOffAllLEDs();
    leds->turnOnAllLEDs({0, 0, 255});
    sensor->prepareForDetection(GAME_SWING_DISTANCE_MIN, GAME_SWING_DISTANCE_MAX);
    sensor->startMeasurement();
    int i = 0;
    while (i < 50) {
        sensor->getMeasurement();
        i++;
    }
    sensorMeasurementReaction = app.onRepeat(10, []() {
        if (sensor->isDataAvailable()) {
            sensor->setDataRead();
            uint16_t distance = sensor->getMeasurement();
            DEBUG_PRINT("DETECTED: ");
            DEBUG_PRINTLN(distance);
            sensor->clearInterruptMask();
            if (distance > GAME_SWING_DISTANCE_THRESHOLD && distance < GAME_SWING_DISTANCE_MAX * 2) {
                while (sensor->isDataAvailable()) {
                    sensor->getMeasurement();
                    sensor->setDataRead();
                    app.tick();
                }
                swingSuccess();
            }
        }
    });

    gameSwingTimeoutReaction = app.onDelay(GAME_SWING_TIMEOUT, []() {
        app.remove(sensorMeasurementReaction);
        app.remove(gameSwingTimeoutReaction);
        DEBUG_PRINTLN("FAILURE: Swing timeout");
        swingFailure();
    });
}

void startGame() {
    DEBUG_PRINTLN("Starting game");
    audio->play(COUNTDOWN_SOUND);
    app.onDelay(3100, []() {
        waitForSwing();
    });
}

//////////////////
void parseNextCommand(int selection);
void debugAudioModule(String args);
void debugLEDModule(String args);
void debugPowerModule(String args);
void debugSensorModule(String args);

void enterDebugMode() {
    DEBUG_PRINTLN("Entering debug mode");
    DEBUG_PRINTLN("-> Please select module to test");
    DEBUG_PRINTLN("1. Audio - args: [play (track:int), pause, stop, vol (level:int), fileCount, isPlaying]");
    DEBUG_PRINTLN("2. LEDs - args: [on (led_index:int), off (led_index:int), color (led_index:int) (red:int) (green:int) (blue:int), offAll, onAll, rainbow, heartbeat]");
    DEBUG_PRINTLN("3. Power - args: [powerOff, battery, indicateBattery (optional -> level:int)]");
    DEBUG_PRINTLN("4. Sensor - args: [swing (measuring_time:int)]");
    DEBUG_PRINTLN("5. Communication [WIP]");

    int selection = 0;
    while (selection < 1 || selection > 5) {
        DEBUG_PRINTLN("Enter selection: ");
        while (!Serial.available()) {
            app.tick();
        }
        selection = Serial.parseInt();
    }
    parseNextCommand(selection);
}

void parseNextCommand(int selection) {
    String args = "";
    DEBUG_PRINTLN("Enter args (to restart enter 'reboot'): ");
    while (!Serial.available()) {
        app.tick();
    }
    args = Serial.readString();
    if (args == "reboot") {
        ESP.restart();
    }
    switch (selection) {
        case 1:
            debugAudioModule(args);
            break;
        case 2:
            debugLEDModule(args);
            break;
        case 3:
            debugPowerModule(args);
            break;
        case 4:
            debugSensorModule(args);
            break;
            // case 5:
            //     enterCommunicationModule();
            //     break;
    }
}

////////////////////////
//      DEBUG MODES
////////////////////////

void debugAudioModule(String args) {
    DEBUG_PRINTLN("Debugging Audio");
    String command = args.substring(0, args.indexOf(' '));
    String arg = args.substring(args.indexOf(' ') + 1);
    if (command == "play") {
        audio->play(arg.toInt());
    } else if (command == "pause") {
        audio->pause();
    } else if (command == "stop") {
        audio->stop();
    } else if (command == "vol") {
        audio->volume(arg.toInt());
    } else if (command == "fileCount") {
        DEBUG_PRINT("File count: ");
        DEBUG_PRINTLN(audio->readFileCount());
    } else if (command == "isPlaying") {
        DEBUG_PRINT("Is playing: ");
        DEBUG_PRINTLN(audio->isPlaying());
    }
    parseNextCommand(1);
}

void debugLEDModule(String args) {
    DEBUG_PRINTLN("Debugging LEDs");
    String command = args.substring(0, args.indexOf(' '));
    String arg = args.substring(args.indexOf(' ') + 1);
    if (command == "on") {
        leds->setLED(arg.toInt(), 255, 255, 255);
    } else if (command == "off") {
        leds->turnOffLED(arg.toInt());
    } else if (command == "color") {
        int led = arg.substring(0, arg.indexOf(' ')).toInt();
        arg = arg.substring(arg.indexOf(' ') + 1);
        int r = arg.substring(0, arg.indexOf(' ')).toInt();
        arg = arg.substring(arg.indexOf(' ') + 1);
        int g = arg.substring(0, arg.indexOf(' ')).toInt();
        arg = arg.substring(arg.indexOf(' ') + 1);
        int b = arg.toInt();
        leds->setLED(led, r, g, b);
    } else if (command == "offAll") {
        leds->turnOffAllLEDs();
    } else if (command == "onAll") {
        leds->turnOnAllLEDs();
    } else if (command == "rainbow") {
        rainbowReaction = app.onRepeat(10, []() {
            leds->rainbow();
        });
        DEBUG_PRINTLN("Rainbow started - after 10 seconds it will stop");
        app.onDelay(10000, []() {
            app.remove(rainbowReaction);
            DEBUG_PRINTLN("Stopping rainbow");
            leds->turnOffAllLEDs();
            parseNextCommand(2);
        });
        return;
    } else if (command == "heartbeat") {
        DEBUG_PRINTLN("Starting heartbeat");
        heartbeatReaction = app.onRepeat(10, []() {
            leds->heartbeat();
        });
        DEBUG_PRINTLN("Heartbeat started - after 10 seconds it will stop");
        app.onDelay(10000, []() {
            app.remove(heartbeatReaction);
            DEBUG_PRINTLN("Stopping heartbeat");
            leds->turnOffAllLEDs();
            parseNextCommand(2);
        });
        return;
    }
    parseNextCommand(2);
}

void debugPowerModule(String args) {
    DEBUG_PRINTLN("Debugging Power");
    String command = args.substring(0, args.indexOf(' '));
    String arg = args.substring(args.indexOf(' ') + 1);
    if (command == "powerOff") {
        power->powerOff();
    } else if (command == "battery") {
        int batteryLevel = power->getChargeStatus();
        DEBUG_PRINT("Battery level: ");
        DEBUG_PRINTLN(batteryLevel);
    } else if (command == "indicateBattery") {
        int level = arg == "" ? power->getChargeStatus() : arg.toInt();
        indicateBatteryLevel(level);
    }
    parseNextCommand(3);
}

void debugSensorModule(String args) {
    DEBUG_PRINTLN("Debugging Sensor");
    String command = args.substring(0, args.indexOf(' '));
    String arg = args.substring(args.indexOf(' ') + 1);
    if (command == "swing") {
        DEBUG_PRINT("Starting detection for ");
        DEBUG_PRINT(arg);
        DEBUG_PRINTLN(" minutes");
        sensor->prepareForDetection(50, 100);
        sensor->startMeasurement();
        sensorMeasurementReaction = app.onRepeat(10, []() {
            if (sensor->isDataAvailable()) {
                sensor->setDataRead();
                DEBUG_PRINT("DETECTED: ");
                DEBUG_PRINTLN(sensor->getMeasurement());
                sensor->clearInterruptMask();
            }
        });

        app.onDelay(arg.toInt() * 60000, []() {
            app.remove(sensorMeasurementReaction);
            DEBUG_PRINTLN("Stopping sensor");
            parseNextCommand(4);
        });
        return;
    }
    parseNextCommand(4);
}

/**
 * Initialize all submodules, (sensors, LEDs, audio and power)
 * Connect to base station
 * Go to main loop
 */
void setup() {
    delay(1000);  // delay for all serial and other module connections to be established

    START_DEBUG;
    DEBUG_PRINTLN("Starting BETH");

    // initialize LEDs
    DEBUG_PRINTLN("Initializing LEDs");
    leds = new LEDs(&ws2812b);
    leds->turnOffAllLEDs();

    // initialize Sensor
    DEBUG_PRINTLN("Initializing Sensor");
    sensor = new Sensor(&TOFsensor, app, VL53LOX_INTERRUPT_PIN_2);
    if (sensor->sensorBootFailed) {
        leds->turnOnAllLEDs({255, 0, 0});
        delay(800);
        ESP.restart();
    }

    // delay(5000);

    // initialize Audio
    DEBUG_PRINTLN("Initializing Audio");
    softwareSerial.begin(9600);
    player.begin(softwareSerial);
    audio = new Audio(&player);
    app.onDelay(100, []() {
        audio->playStartUpSound();
    });
    app.onDelay(2000, []() {
        audio->volume(30);
    });

    // initialize Power
    DEBUG_PRINTLN("Initializing Power");
    power = new Power();
    setupBattery();

    DEBUG_PRINTLN("ALL MODULES INITIALIZED");
    app.onDelay(3000, []() {
        connectToBaseStation();
    });

    app.onDelay(15000, []() {
        startGame();
    });
    // enterDebugMode();
}

void loop() {
    app.tick();
}