from abc import ABC, abstractmethod

class WeatherInterface(ABC):
    @abstractmethod
    def get_weather(self, city: str):
        pass  # Returns weather data as a plain text

class OldWeatherAPI(WeatherInterface):
    def get_weather(self, city: str):
        if city == "":
            raise ValueError("City name cannot be empty.")
        # Simulating weather information for different cities
        return f"The weather in {city} today is sunny with a temperature of 25°C."
