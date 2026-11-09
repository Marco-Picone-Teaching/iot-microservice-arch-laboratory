# Emulated IoT device publishing temperature telemetry (Paho MQTT 2.x).
# From the mqtt-tester folder run: uv run mqtt-device-producer [device_id]
# The MQTT Data Fetcher forwards each telemetry message to the IoT Inventory API.

import sys
import threading
import time
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from mqtt_tester.model.message_descriptor import MessageDescriptor
from mqtt_tester.model.temperature_sensor import TemperatureSensor
from mqtt_tester.tester_config import load_broker_configuration

# Configuration variables
default_device_id = "d0001"
topic_template = "device/{}/temperature"
message_limit = 1000
publish_period_s = 5

# Set by the on_connect callback when the connection has been accepted by the broker
connected_event = threading.Event()


def on_connect(client: mqtt.Client, userdata: Any, flags: mqtt.ConnectFlags,
               reason_code: ReasonCode, properties: Properties | None) -> None:
    print(f"Connected with result code {reason_code}")
    if not reason_code.is_failure:
        connected_event.set()


def main() -> None:

    device_id = sys.argv[1] if len(sys.argv) > 1 else default_device_id
    topic = topic_template.format(device_id)
    broker = load_broker_configuration()

    # Create the MQTT client using the device id in the client id (it must be unique on the broker)
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, f"{device_id}-producer")
    mqtt_client.on_connect = on_connect

    if broker["username"] and broker["password"]:
        mqtt_client.username_pw_set(broker["username"], broker["password"])

    print(f"Connecting to {broker['broker_ip']} port: {broker['broker_port']}")
    mqtt_client.connect(broker["broker_ip"], broker["broker_port"])

    # Start the network loop in a background thread and wait for the CONNACK before publishing
    mqtt_client.loop_start()
    if not connected_event.wait(timeout=10):
        print("Connection to the broker failed")
        mqtt_client.loop_stop()
        return

    temperature_sensor = TemperatureSensor()

    try:
        for message_id in range(message_limit):
            temperature_sensor.measure_temperature()
            payload_string = MessageDescriptor(int(time.time()),
                                               "TEMPERATURE_SENSOR",
                                               temperature_sensor.temperature_value).to_json()

            message_info = mqtt_client.publish(topic, payload_string)
            message_info.wait_for_publish()
            print(f"Message Sent: {message_id} Topic: {topic} Payload: {payload_string}")
            time.sleep(publish_period_s)
    except KeyboardInterrupt:
        print("Producer stopped")
    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()


if __name__ == "__main__":
    main()
