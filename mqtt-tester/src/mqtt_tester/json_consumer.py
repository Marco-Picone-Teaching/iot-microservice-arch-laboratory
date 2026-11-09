# MQTT consumer printing the telemetry published by all the devices (Paho MQTT 2.x).
# From the mqtt-tester folder run: uv run mqtt-telemetry-consumer
# Useful to check the messages flowing through the broker independently of the other services.

import json
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from mqtt_tester.model.message_descriptor import MessageDescriptor
from mqtt_tester.tester_config import load_broker_configuration

# Configuration variables
client_id = "mqtt-tester-consumer"
target_topic_filter = "device/+/temperature"


def on_connect(client: mqtt.Client, userdata: Any, flags: mqtt.ConnectFlags,
               reason_code: ReasonCode, properties: Properties | None) -> None:
    print(f"Connected with result code {reason_code}")
    if reason_code.is_failure:
        client.disconnect()
        return
    client.subscribe(target_topic_filter)
    print(f"Subscribed to: {target_topic_filter}")


def on_message(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        message_payload = message.payload.decode("utf-8")
        message_descriptor = MessageDescriptor(**json.loads(message_payload))
        print(f"Received IoT Message: Topic: {message.topic} Timestamp: {message_descriptor.timestamp} "
              f"Type: {message_descriptor.data_type} Value: {message_descriptor.value}")


def main() -> None:

    broker = load_broker_configuration()

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    if broker["username"] and broker["password"]:
        mqtt_client.username_pw_set(broker["username"], broker["password"])

    mqtt_client.connect(broker["broker_ip"], broker["broker_port"])

    # Blocking network loop: processes the network traffic, dispatches the callbacks and handles the reconnections
    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        print("Consumer stopped")


if __name__ == "__main__":
    main()
