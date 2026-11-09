from iot_inventory_api.dto.telemetry_message import TelemetryMessage


class DataManager:
    """
    DataManager class is responsible for managing the data of the application.
    Abstracts the data storage and retrieval operations.
    In this implementation everything is stored in memory.
    """

    def __init__(self) -> None:
        # Telemetry data (time series) indexed by the device id
        self.device_timeseries_data: dict[str, list[TelemetryMessage]] = {}

    def add_device_telemetry_data(self, device_id: str, telemetry_data: TelemetryMessage) -> None:
        """Add a new telemetry data for a given device"""
        if device_id not in self.device_timeseries_data:
            self.device_timeseries_data[device_id] = []
        self.device_timeseries_data[device_id].append(telemetry_data)

    def get_telemetry_data_by_device_id(self, device_id: str) -> list[TelemetryMessage] | None:
        """Return the telemetry data for a given device (None if the device has never sent data)"""
        return self.device_timeseries_data.get(device_id)
