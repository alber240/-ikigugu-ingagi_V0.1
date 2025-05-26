#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Network settings (replace with your LAN details if available)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 177);
const char* mqtt_server = "broker.hivemq.com"; 
const int mqtt_port = 1883;
const char* mqtt_client_id = "ArduinoFan1";
const char* control_topic = "smartlab/fan1/control";
const char* status_topic = "smartlab/fan1/status";


const int relayPin = 7;

// MQTT client
EthernetClient ethClient;
PubSubClient client(ethClient);

void setup() {
  // Initialize relay pin (or LED for simulation)
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  // Start Ethernet (simulated in Tinkercad)
  Ethernet.begin(mac, ip);

  // Connect to MQTT broker
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Connect to MQTT
  reconnect();
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect(mqtt_client_id)) {
      client.subscribe(control_topic);
      client.publish(status_topic, "off"); 
    } else {
      delay(5000); 
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Parse MQTT message
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // Handle commands
  if (message == "on") {
    digitalWrite(relayPin, HIGH);
    client.publish(status_topic, "on");
  } else if (message == "off") {
    digitalWrite(relayPin, LOW); 
    client.publish(status_topic, "off");
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Simulate time-based schedule
  static unsigned long lastCheck = 0;
  if (millis() - lastCheck > 60000) {

    digitalWrite(relayPin, LOW);
    client.publish(status_topic, "off");
    lastCheck = millis();
  }
}
