#include <PubSubClient.h>
#include <Ethernet.h>
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetClient ethClient;
PubSubClient client(ethClient);
const char* mqtt_server = "192.168.1.100"; // Update with broker IP
const int relayPin = 7;

void setup() {
  pinMode(relayPin, OUTPUT);
  Ethernet.begin(mac);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  client.subscribe("smartlab/fan1");
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) message += (char)payload[i];
  if (message == "on") digitalWrite(relayPin, HIGH); // LED on
  else if (message == "off") digitalWrite(relayPin, LOW); // LED off
}

void loop() {
  if (!client.connected()) client.connect("ArduinoClient");
  client.loop();
}
