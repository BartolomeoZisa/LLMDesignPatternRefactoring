import pytest
from alternative.Weather import OldWeatherAPI  # Make sure to import OldWeatherAPI from the correct module

# Test case to verify if OldWeatherAPI returns the correct weather info for a valid city
def test_get_weather_valid_city():
    # Instantiate the OldWeatherAPI
    old_weather_api = OldWeatherAPI()
    
    # Define a valid city
    city = "New York"
    
    # Call the get_weather method
    result = old_weather_api.get_weather(city)
    
    # Expected result for the given city
    expected_result = "The weather in New York today is sunny with a temperature of 25°C."
    
    # Assert that the result matches the expected result
    assert result == expected_result

# Test case to verify that ValueError is raised when an empty city name is passed
def test_get_weather_empty_city():
    # Instantiate the OldWeatherAPI
    old_weather_api = OldWeatherAPI()
    
    # Define an empty city name
    city = ""
    
    # Assert that ValueError is raised when an empty city name is provided
    with pytest.raises(ValueError) as excinfo:
        old_weather_api.get_weather(city)
    
    # Check if the exception message is as expected
    assert str(excinfo.value) == "City name cannot be empty."

# Test case to verify if OldWeatherAPI works for other valid cities
def test_get_weather_other_valid_city():
    # Instantiate the OldWeatherAPI
    old_weather_api = OldWeatherAPI()
    
    # Define another valid city
    city = "London"
    
    # Call the get_weather method
    result = old_weather_api.get_weather(city)
    
    # Expected result for the given city
    expected_result = "The weather in London today is sunny with a temperature of 25°C."
    
    # Assert that the result matches the expected result
    assert result == expected_result