#include <Arduino.h>
#include <WiFi.h>

// pin definitions
#define WIFI_LED LED_BUILTIN
#define STATUS_LED 14
#define ECHO_PIN 13
#define TRIG_PIN 12
#define KILL_SWITCH 27

// message codes
#define OK 0x0
#define DISCONNECT 0x11
#define MOTION_DETECTED 0x12

#define SSID ""
#define PASS ""
#define PORT_NO 20000
// the speed of sound in cm/µs
#define SOUND_SPEED 0.0343

float get_distance();

void setup(){
  // set up pins
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(KILL_SWITCH, INPUT_PULLDOWN);
  // connect to WiFi
  Serial.begin(9600);
  Serial.println("Connecting...");
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".....");
  }
  // indicate the wifi is connected
  Serial.print("Connected\nLocal IP: ");
  Serial.println(WiFi.localIP());
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop(){
  // find the inital distance from the wall/door
  float init_distance = get_distance();
  // setup the server
  WiFiServer server(PORT_NO);
  server.begin();
  // await a connection from a client
  WiFiClient client;
  while (!client)
    client = server.available();
  digitalWrite(STATUS_LED, HIGH);
  // run the server
  bool enabled = true;
  unsigned char response;
  while (enabled){
    // check if something is in front of the sensor (within 5cm of accuracy)
    if ((init_distance - get_distance()) >= 5){
      client.write(MOTION_DETECTED);
      client.readBytes(&response, 1);
      delay(500);
      if ((int) response != 0x0){
        enabled = false;
        Serial.printf("Response: %x\nDisabling...\n", response);
      }
    }
    if (!digitalRead(KILL_SWITCH))
      enabled = false;
  }
  // kill the connection when the sensor has been enabled
  digitalWrite(STATUS_LED, LOW);
  client.write(DISCONNECT);
}

// reads the distance from the distance sensor
float get_distance(){
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  float duration = pulseIn(ECHO_PIN, HIGH);
  // calculate the distance traveled (speed of sound = 0.343mm/µs)
  return (duration*SOUND_SPEED)/2;
}
