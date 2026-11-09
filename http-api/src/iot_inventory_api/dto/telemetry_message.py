import json


class TelemetryMessage:
    """
    Telemetry Message DTO class mapping the JSON body of the telemetry data exchanged through the RESTful API:
    - timestamp: timestamp of the telemetry message
    - data_type: type of the telemetry message
    - value: value of the telemetry message
    """

    def __init__(self, timestamp: int, data_type: str, value: float) -> None:
        self.timestamp = timestamp
        self.data_type = data_type
        self.value = value

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
