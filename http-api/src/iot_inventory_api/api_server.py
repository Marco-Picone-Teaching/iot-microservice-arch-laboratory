# IoT Inventory RESTful HTTP API microservice. From the service folder run: uv run iot-inventory-api
# In the container the same command is the CMD of the Docker image.

import signal
import sys
from types import FrameType
from typing import Any

from flask import Flask
from flask_restful import Api
from werkzeug.serving import make_server

from iot_inventory_api.config.config_loader import ConfigLoader
from iot_inventory_api.persistence.data_manager import DataManager
from iot_inventory_api.resources.telemetry_data_resource import TelemetryDataResource

# Configuration file (searched in the working directory and in the service root)
CONF_FILE_PATH = "conf.yaml"

# Default configuration, used for the parameters not defined in the configuration file
DEFAULT_CONFIGURATION: dict[str, Any] = {
    "rest": {
        "api_prefix": "/api/v1/iot/inventory",
        "host": "0.0.0.0",
        "port": 7070
    }
}


def create_app(data_manager: DataManager, api_prefix: str) -> Flask:
    """ Create the Flask application with the RESTful API resources """

    app = Flask(__name__)
    api = Api(app)
    # Telemetry Data of a specific device
    api.add_resource(TelemetryDataResource, api_prefix + '/device/<string:device_id>/telemetry',
                     resource_class_kwargs={'data_manager': data_manager},
                     endpoint="device_telemetry_data",
                     methods=['GET', 'POST'])

    return app


def handle_sigterm(signum: int, frame: FrameType | None) -> None:
    """ Stop the service when the container is stopped (docker stop sends SIGTERM to the main process) """
    sys.exit(0)


def main() -> None:

    configuration = ConfigLoader.load(CONF_FILE_PATH, DEFAULT_CONFIGURATION)
    rest_configuration = configuration["rest"]

    # Data Manager storing the telemetry data in memory
    data_manager = DataManager()

    app = create_app(data_manager, rest_configuration["api_prefix"])

    # In a container the process has PID 1 and ignores SIGTERM unless a handler is installed
    signal.signal(signal.SIGTERM, handle_sigterm)

    http_server = make_server(rest_configuration["host"], rest_configuration["port"], app, threaded=True)
    print(f"IoT Inventory API running on http://{rest_configuration['host']}:{rest_configuration['port']}"
          f"{rest_configuration['api_prefix']} (CTRL+C to stop)")

    try:
        http_server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print("IoT Inventory API stopped")
    finally:
        http_server.server_close()


if __name__ == "__main__":
    main()
