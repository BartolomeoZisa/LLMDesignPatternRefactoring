import json
from abc import ABC, abstractmethod

# Abstract Weather Interface that requires a `get_weather` method
class WeatherInterface(ABC):
    @abstractmethod
    def get_weather(self, city: str):
        pass  # Returns weather data as a plain text
    def testname(self, city: str):
        if city == "":
            raise ValueError("City name cannot be empty.")

# Old Weather API that returns weather info for a city in plain text
class OldWeatherAPI(WeatherInterface):
    def get_weather(self, city: str):
        # Simulating weather information for different cities
        self.testname(city)
        return f"The weather in {city} today is sunny with a temperature of 25°C."

# New Weather API that returns weather info for a city in JSON format
class NewWeatherAPI:
    def get_weather_json(self, city: str):
        # Simulating a JSON response from an external weather API based on city
        weather_data = {
            "city": city,
            "temperature": 25,
            "description": "sunny",
            "humidity": 60
        }
        return json.dumps(weather_data)

# Weather API Adapter that converts the new API's JSON response to the old text format
class WeatherAPIAdapter(WeatherInterface):
    def __init__(self, new_api: NewWeatherAPI):
        self.new_api = new_api
    
    def get_weather(self, city: str):
        # Call the new API which returns JSON for the given city
        weather_json = self.new_api.get_weather_json(city)
        
        # Parse the JSON data
        weather_data = json.loads(weather_json)
        
        # Extract relevant fields
        temperature = weather_data["temperature"]
        description = weather_data["description"]
        
        self.testname(city)

        # Convert the data to the expected text format
        return f"The weather in {city} today is {description} with a temperature of {temperature}°C."

