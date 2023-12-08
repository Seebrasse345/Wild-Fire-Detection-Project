#include <SimpleDHT.h>
#include <MKRWAN.h>
#include <CayenneLPP.h>

LoRaModem modem;
CayenneLPP lpp(120); // Cayenne byte limit
int pinDHT22 = 3;
int batteryPin = A0; // Analog pin for battery voltage

String appEui = "A8610A32303F7904";
String appKey = "AF17D1957204236D0835DB8E80462948";
SimpleDHT22 dht22(pinDHT22);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  modem.minPollInterval(60);
  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };
  uint32_t timeout = 90000;
  int connected = modem.joinOTAA(appEui, appKey, timeout);

  if (!connected) {
    Serial.println("Something went wrong; are you indoor? Move near a window and retry");
  }
  if (connected) {
    Serial.println("Connected");
  }
  delay(5000);
}

void loop() {
  float temperature = 0;
  float humidity = 0;
  int err_dht = SimpleDHTErrSuccess;
  if ((err_dht = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT22 failed, err_dht="); Serial.print(SimpleDHTErrCode(err_dht));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err_dht)); delay(2000);
    return;
  }

  float batteryVoltage = readBatteryVoltage();
  if (batteryVoltage < 0) {
    Serial.println("Failed to read battery voltage");
    return;
  }

  message_sender(temperature, humidity, batteryVoltage);
  delay(60000);
}

float readBatteryVoltage() {
    int sensorValue = analogRead(A0); // Replace A0 with your actual analog pin
    float batteryVoltage = sensorValue * (3.3 / 1023.0); // Convert to voltage
    return batteryVoltage;
}


void message_sender(float temp, float humidity, float batteryVoltage) {
  lpp.reset();
  lpp.addTemperature(1, temp);
  lpp.addRelativeHumidity(2, humidity);
  lpp.addAnalogInput(3, batteryVoltage); // Add battery voltage to payload

  Serial.println(String(humidity) + "%");
  Serial.println(String(temp) + "*C");
  Serial.println(String(batteryVoltage) + "V");

  modem.beginPacket(); // Begin the packet without checking for a return value
  modem.write(lpp.getBuffer(), lpp.getSize());
  int err = modem.endPacket(true); // Check for errors after sending the packet

  if (err > 0) {
    Serial.println("Message sent correctly!");
  } else {
    Serial.println("Error sending message :(");
    Serial.println("(you may send a limited amount of messages per minute, depending on the signal strength");
    Serial.println("it may vary from 1 message every couple of seconds to 1 message every minute)");
  }
}

