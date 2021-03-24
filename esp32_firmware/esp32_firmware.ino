/**
 * @author Carlos Soto Pérez <carlos348@outlook.com>
 * Para la ESP32. Conexión a una red WiFi y publicación de datos de sensores y datos desde BLE
 * en ThingSpeak
 */
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <ThingSpeak.h>
#include <WiFi.h>

WiFiClient wClient;
#define CHANEL_ID 0
#define WRITE_KEY ""

int scanTime = 5; //In seconds
BLEScan* pBLEScan;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
    }
};

void initBLEScan() {
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);
}

void connectToWiFi(const char* ssid, const char* password) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected, my local IP is:");
  Serial.println(WiFi.localIP());
}

void setup(void)
{
  const char* ssid = "";
  const char* password = "";
  Serial.begin(115200);
  initBLEScan();
  connectToWiFi(ssid, password);
  ThingSpeak.begin(wClient);
}

void filterBLEAddress(BLEScanResults foundDevices) {
  String testAddress[] = {
    "ff:ff:44:46:5f:47",
    "ff:ff:c0:16:47:9a",
    "ff:ff:ff:f0:d8:c4"
  };
  int deviceCount = foundDevices.getCount();
  for(int i = 0; i < deviceCount; i++) {
    BLEAdvertisedDevice device = foundDevices.getDevice(i);
    int txPower = device.getTXPower();
    String address = device.getAddress().toString().c_str();
    for (int j = 0; j < 3; j++) {
      if(address.compareTo(testAddress[j]) == 0) {
        ThingSpeak.setField(i + 1, txPower);
        return;
      }
    }
  }
}

void scanBLETags() {
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  filterBLEAddress(foundDevices);
}

void loop() {
  // put your main code here, to run repeatedly:
  scanBLETags();
  ThingSpeak.writeFields(CHANEL_ID, WRITE_KEY);
  Serial.println("Data sent to TS");
  delay(5000);
}