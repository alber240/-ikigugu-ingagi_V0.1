import paho.mqtt.client as mqtt
import time
import json
import datetime

# Configuration
broker = "broker.hivemq.com"  
devices = ["pc1", "projector1"] 
device_states = {device: "off" for device in devices}  
log_file = "device_logs.json"  

# Log device actions
def log_action(device, action):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "device": device,
        "action": action,
        "state": device_states[device]
    }
    with open(log_file, "a") as f:
        json.dump(log_entry, f)
        f.write("\n")
    print(f"Logged: {log_entry}")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with code {rc}")
    for device in devices:
        client.subscribe(f"smartlab/{device}/control")
    client.subscribe("smartlab/all/control") 

def on_message(client, userdata, msg):
    topic = msg.topic
    command = msg.payload.decode()
    print(f"Received: {topic} -> {command}")


    for device in devices:
        if topic == f"smartlab/{device}/control":
            if command in ["on", "off"]:
                device_states[device] = command
                log_action(device, f"Received {command}")
                client.publish(f"smartlab/{device}/status", device_states[device])
            elif command == "status":
                client.publish(f"smartlab/{device}/status", device_states[device])

    if topic == "smartlab/all/control" and command == "off":
        for device in devices:
            device_states[device] = "off"
            log_action(device, "Group shutdown")
            client.publish(f"smartlab/{device}/status", "off")

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)

# Simulate device behavior
client.loop_start()
print(f"Simulating devices: {devices}")
while True:

    for device in devices:
        client.publish(f"smartlab/{device}/status", device_states[device])
    time.sleep(60)
