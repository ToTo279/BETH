#ifndef SENSOR_H
#define SENSOR_H

#include <Arduino.h>
#include <Adafruit_VL53L0X.h>
#include <ReactESP.h>
#include <Wire.h>

class Sensor {
   private:
    Adafruit_VL53L0X* loxSensor;
    VL53L0X_RangingMeasurementData_t measure;
    volatile bool newData = false;

   public:
    bool sensorBootFailed = false;
    int INTERRUPT_PIN;
    Sensor(Adafruit_VL53L0X* sensor, reactesp::ReactESP &app, int interruptPin);
    ~Sensor();
    void onInterrupt();
    void setInterruptThreshold(int lower, int upper);
    void setDeviceMode(VL53L0X_DeviceModes deviceMode);
    void startMeasurement();
    uint16_t getMeasurement();
    bool isDataAvailable();
    void clearInterruptMask();
    void prepareForDetection(int lower, int upper);
    void setDataRead();
    void stopMeasurement();
};

#endif