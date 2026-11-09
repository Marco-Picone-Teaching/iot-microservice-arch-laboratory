import random


class TemperatureSensor:
    """ Emulated temperature sensor generating random values between 20.0 and 40.0 """

    def __init__(self) -> None:
        self.temperature_value: float = 0.0
        self.measure_temperature()

    def measure_temperature(self) -> None:
        self.temperature_value = random.uniform(20.0, 40.0)
