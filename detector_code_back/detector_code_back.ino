#include <SimpleDHT.h>
#include <MKRWAN.h>
#include <CayenneLPP.h>

LoRaModem modem;
<<<<<<< Updated upstream
CayenneLPP lpp(120); //cayenne bite limit
=======
CayenneLPP lpp(120); // Cayenne byte limit
const float resistor2 = 10000.0;
const float resistor1= 1000.0;
const float referencev = 3.3;
>>>>>>> Stashed changes
int pinDHT22 = 3;

String appEui;
String appKey;

SimpleDHT22 dht22(pinDHT22);

void setup() {
  Serial.begin(115200);
  
  modem.minPollInterval(60);
  
  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };
  
String deviceEUI = modem.deviceEUI();
deviceEUI.trim();
deviceEUI.toLowerCase();

if (deviceEUI == "a8610a32303f7904") {
  appEui = "A8610A32303F7904";
  appKey = "AF17D1957204236D0835DB8E80462948";
} else if (deviceEUI == "a8610a32343e7c10") {
  appEui = "A8610A32343E7C10";
  appKey = "F18E4D32FE6E240CF814D967E7C89384";
} else {
  Serial.println("Unknown device EUI");
  while (1) {}
}
  uint32_t timeout = 90000;
<<<<<<< Updated upstream
  int connected = modem.joinOTAA(appEui, appKey,timeout);

  
=======
  int connected = modem.joinOTAA(appEui, appKey, timeout);
>>>>>>> Stashed changes
  if (!connected) {
     Serial.println("Something went wrong; are you indoor? Move near a window and retry");
  }
<<<<<<< Updated upstream
  if(connected){
=======
  
  if (connected) {
>>>>>>> Stashed changes
    Serial.println("Connected");
  }
  
  delay(5000);
  }
 
  //2 minute time interval is hard wired eitherways

void message_sender(float temp,float humidity){
  lpp.reset();
  lpp.addTemperature(1,temp);
  lpp.addRelativeHumidity(2, humidity);
  // for some reason cayenne lpp doubles humidity
  Serial.println(String(humidity) + "%");
  Serial.println(String(temp) + "*C");
 
  
  int err;
  modem.beginPacket();
  modem.write(lpp.getBuffer(),lpp.getSize());
  err = modem.endPacket(true);
  if (err > 0) {
    Serial.println("Message sent correctly!");
  } 
  else {
    Serial.println("Error sending message :(");
    Serial.println("(you may send a limited amount of messages per minute, depending on the signal strength");
    Serial.println("it may vary from 1 message every couple of seconds to 1 message every minute)");

  }

}
void loop() {
  // put your main code here, to run repeatedly:
  float temperature = 0;
  float humidity = 0;
  int err_dht = SimpleDHTErrSuccess;
<<<<<<< Updated upstream
  //error management for moisture probe
=======
  
>>>>>>> Stashed changes
  if ((err_dht = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT22 failed, err_dht=");
    Serial.print(SimpleDHTErrCode(err_dht));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err_dht)); delay(2000);
    return;
  }
<<<<<<< Updated upstream
  //for some reason lpp doubles it?
  message_sender(temperature,humidity);
=======
  
  float batteryVoltage = readBatteryVoltage();
  if (batteryVoltage < 0) {
    Serial.println("Failed to read battery voltage");
    return;
  }
  
  message_sender(temperature, humidity, batteryVoltage);
>>>>>>> Stashed changes
  delay(60000);





  


}
<<<<<<< Updated upstream
=======

float readBatteryVoltage() {
  int sensorValue = analogRead(batteryPin);
  float measuredVoltage = sensorValue * (referencev / 1024.0);
  float batteryVoltage = measuredVoltage*((resistor1+resistor2)/resistor2); // Assuming equal resistor values
  return batteryVoltage;
}

void message_sender(float temp, float humidity, float batteryVoltage) {
  lpp.reset();
  lpp.addTemperature(1, temp);
  lpp.addRelativeHumidity(2, humidity);
  lpp.addAnalogInput(3, batteryVoltage);
  
  Serial.println(String(humidity) + "%");
  Serial.println(String(temp) + "*C");
  Serial.println(String(batteryVoltage) + "V");
  
  modem.beginPacket();
  modem.write(lpp.getBuffer(), lpp.getSize());
  int err = modem.endPacket(true);
  
  if (err > 0) {
    Serial.println("Message sent correctly!");
  } else {
    Serial.println("Error sending message :(");
    Serial.println("(you may send a limited amount of messages per minute, depending on the signal strength");
    Serial.println("it may vary from 1 message every couple of seconds to 1 message every minute)");
  }
}
>>>>>>> Stashed changes
