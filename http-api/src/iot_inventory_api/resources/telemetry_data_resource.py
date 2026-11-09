from json import JSONDecodeError
from typing import Any

from flask import request, Response
from flask_restful import Resource

from iot_inventory_api.dto.telemetry_message import TelemetryMessage
from iot_inventory_api.persistence.data_manager import DataManager


class TelemetryDataResource(Resource):
    """Resource to handle the Telemetry Data of a specific Device: read (GET) and add (POST) telemetry data"""

    def __init__(self, **kwargs: Any) -> None:
        # Inject the DataManager instance
        self.data_manager: DataManager = kwargs['data_manager']

    def get(self, device_id: str) -> Any:
        """GET Request to retrieve the Telemetry Data of a target device"""

        device_telemetry_data = self.data_manager.get_telemetry_data_by_device_id(device_id)

        if device_telemetry_data is None:
            return {'error': "Device Not Found !"}, 404

        # Build a serializable list transforming each telemetry data into a dictionary:
        # Flask-RESTful then serializes it into JSON
        return [telemetry_data.__dict__ for telemetry_data in device_telemetry_data], 200

    def post(self, device_id: str) -> Any:
        """POST Request to add a new Telemetry Data to a target device"""
        try:
            # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)

            # Deserialize the body into the TelemetryMessage DTO: a body with missing or unknown fields is rejected
            telemetry_message = TelemetryMessage(**json_data)

            self.data_manager.add_device_telemetry_data(device_id, telemetry_message)

            return Response(status=201)  # 201 Created

        except (JSONDecodeError, TypeError):
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
