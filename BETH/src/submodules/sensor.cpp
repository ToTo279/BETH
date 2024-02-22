#include "sensor.h"

#include "config.h"
#include "debug.h"

Sensor::Sensor(Adafruit_VL53L0X* sensor, reactesp::ReactESP& app, int interruptPin) {
    DEBUG_PRINTLN("[Sensor] Sensor Initializing");
    this->loxSensor = sensor;
    this->INTERRUPT_PIN = interruptPin;
    pinMode(INTERRUPT_PIN, INPUT_PULLUP);
    app.onInterrupt(INTERRUPT_PIN, RISING, [this]() { this->onInterrupt(); });

    if (!this->loxSensor->begin(VL53L0X_I2C_ADDR, true)) {
        DEBUG_PRINTLN("[CRITICAL][Sensor] Failed to boot VL53L0X");
        sensorBootFailed = true;
    }

    this->loxSensor->setGpioConfig(VL53L0X_DEVICEMODE_CONTINUOUS_RANGING,
                                   VL53L0X_GPIOFUNCTIONALITY_THRESHOLD_CROSSED_HIGH,
                                   VL53L0X_INTERRUPTPOLARITY_HIGH);
}

Sensor::~Sensor() {
    delete loxSensor;
}

void Sensor::onInterrupt() {
    this->newData = true;
}

void Sensor::prepareForDetection(int lower, int upper) {
    DEBUG_PRINTLN("[Sensor] Preparing for detection");
    this->setInterruptThreshold(lower, upper);
    this->setDeviceMode(VL53L0X_DEVICEMODE_CONTINUOUS_RANGING);
    bool res = this->loxSensor->configSensor(Adafruit_VL53L0X::VL53L0X_SENSE_HIGH_SPEED);
    if (!res) {
        DEBUG_PRINTLN("[Sensor] Failed to configure sensor");
    }
    res = this->loxSensor->setMeasurementTimingBudgetMicroSeconds(20 * 1000);  // 20ms
    if (!res) {
        DEBUG_PRINTLN("[Sensor] Failed to set measurement timing budget");
    }
}

void Sensor::setDeviceMode(VL53L0X_DeviceModes deviceMode = VL53L0X_DEVICEMODE_CONTINUOUS_RANGING) {
    DEBUG_PRINTLN("[Sensor] Setting device mode");
    VL53L0X_Error res = loxSensor->setDeviceMode(deviceMode);
    if (res != VL53L0X_ERROR_NONE) {
        DEBUG_PRINTLN("[Sensor] Failed to set device mode");
    }
}

void Sensor::setInterruptThreshold(int lower, int upper) {
    DEBUG_PRINTLN("[Sensor] Setting interrupt thresholds");
    VL53L0X_Error res = loxSensor->setInterruptThresholds((FixPoint1616_t)(lower * VL53LOX_OFFSET), (FixPoint1616_t)(upper * VL53LOX_OFFSET), false);
    if (res != VL53L0X_ERROR_NONE) {
        DEBUG_PRINTLN("[Sensor] Failed to set interrupt thresholds");
    }
}

void Sensor::startMeasurement() {
    DEBUG_PRINTLN("[Sensor] Starting measurement");
    VL53L0X_Error res = loxSensor->startMeasurement(false);
    if (res != VL53L0X_ERROR_NONE) {
        DEBUG_PRINTLN("[Sensor] Failed to start measurement");
    }
}

uint16_t Sensor::getMeasurement() {
    loxSensor->getRangingMeasurement(&measure, false);
    if (measure.RangeStatus == 4) {
        return 0;
    }
    // DEBUG_PRINTLN(measure.RangeMilliMeter);
    return measure.RangeMilliMeter;
}

bool Sensor::isDataAvailable() {
    return newData;
}

void Sensor::setDataRead() {
    newData = false;
}

void Sensor::clearInterruptMask() {
    loxSensor->clearInterruptMask(false);
}

void Sensor::stopMeasurement() {
    loxSensor->stopMeasurement();
}