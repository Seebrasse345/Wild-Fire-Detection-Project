#include <SimpleDHT.h>
#include <MKRWAN.h>
#include <CayenneLPP.h>
#define LPP_RELATIVE_HUMIDITY_SIZE 4
LoRaModem modem;
CayenneLPP lpp(120); //cayenne bite limit
int pinDHT22 = 3;

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
  int connected = modem.joinOTAA(appEui, appKey,timeout);

  
  if (!connected) {
     Serial.println("Something went wrong; are you indoor? Move near a window and retry");
  }
  if(connected){
    Serial.println("Connected");
  }
  delay(5000);
  }
 
  //2 minute time interval is hard wired eitherways

void message_sender(float temp,float humidity){
  lpp.reset();
  lpp.addTemperature(1,temp);
  // for some reason cayenne lpp doubles humidity
  Serial.println(String(humidity) + "%");
  Serial.println(String(temp) + "*C");
  humidity = humidity/2 ;
  lpp.addRelativeHumidity(2, humidity);
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
  //error management for moisture probe
  if ((err_dht = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT22 failed, err_dht="); Serial.print(SimpleDHTErrCode(err_dht));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err_dht)); delay(2000);
    return;
  }
  //for some reason lpp doubles it?
  message_sender(temperature,humidity);
  delay(60000);





  


}
