import json


class MessageDescriptor:
    """ JSON payload of the telemetry messages published by the emulated devices """

    def __init__(self, timestamp: int, data_type: str, value: float) -> None:
        self.timestamp = timestamp
        self.data_type = data_type
        self.value = value

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
