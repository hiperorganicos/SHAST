#include <dht11.h>
#include <yunOSC.h>
#include <Process.h>

#define IP_ADR "146.164.80.56"
//#define IP_ADR "10.32.0.37"
#define PORT 22244

//pins
#define DHT11_PIN 7

int LDR_PIN = A2;
int MOI_PIN = A0;
int DHT_PIN = 7; //Pino DATA do Sensor ligado na porta Analogica A1


dht11 DHT;

//storage vals
int ldr = 0;
int moi = 0;
int chk;
float temp = 0;
float humd = 0;


void setup() {
  // Initialize Bridge
  Bridge.begin();
  
  // make udp connection
  osc.begin(IP_ADR, PORT);
  
  delay(1000);
}

void loop() {
  ldr = analogRead(LDR_PIN);
  moi = analogRead(MOI_PIN);
  chk = DHT.read(DHT11_PIN);
  temp = DHT.temperature;
  humd = DHT.humidity;
  
  runSender("/shast/luz", ldr);
  delay(350);
  
  runSender("/shast/umidadeSolo", moi);
  delay(350);

  runSender("/shast/temperatura", (int)temp);
  delay(350);

  runSender("/shast/umidadeAr", (int)humd);
  delay(350);

  delay(100);
}

void runSender(String addr, int val) {
  int values[1];
  values[0] = val;
  osc.send(addr, values, 1);
}
