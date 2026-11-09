from typing import Any

from mqtt_tester.config.config_loader import ConfigLoader

# Configuration file with the MQTT Broker used by the testers
CONF_FILE_PATH = "tester_conf.yaml"


def load_broker_configuration() -> dict[str, Any]:
    """ Load the broker parameters (broker_ip, broker_port, username, password) """
    return ConfigLoader.load(CONF_FILE_PATH, {"broker_ip": "127.0.0.1", "broker_port": 1883,
                                              "username": None, "password": None})
