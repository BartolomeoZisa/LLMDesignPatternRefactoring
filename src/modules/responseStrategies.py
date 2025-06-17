import os
from abc import ABC, abstractmethod
from openai import OpenAI
from google import genai
from google.genai import types
import sys
import traceback
import re
from src.modules.responseFactory import ResponseStrategyRegistry

api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")



class ResponseStrategy(ABC):
    
    def __init__(self, model_name: str = "gpt-4o-mini-2024-07-18", temperature: float = 1, max_length: int = 2048):
        self.model_name = model_name
        self.temperature = temperature
        self.max_length = max_length


    @abstractmethod
    def process(self, prompt: str) -> str: 
        """Process the prompt and return a response."""
        pass
    def length(self, response : str) -> int:
        """Returns the length of the response."""
        try:
            return len(response.split(" "))
        except AttributeError:
            print("Error: response is not a string or is None.")
            return 0
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 0

class ResponseFromCLI(ResponseStrategy):

    def process(self, prompt):
        print(prompt)
        print("\nEnter the refactored code (type 'DONE' to finish current refactor):")
        refactored_code = ""
        
        # Collect multi-line input
        while True:
            line = input()
            if line.strip() == "DONE":
                break
            refactored_code += line + "\n"
        
        return refactored_code
        

@ResponseStrategyRegistry.register("openai")
class OpenAIResponse(ResponseStrategy):

    def __init__(self, model_name: str = "gpt-4o-mini-2024-07-18", temperature: float = 1, max_length: int = 2048):
        super().__init__()
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.client.debug = True  # Enable debug mode for detailed logging


    def process(self, prompt):
        """Use the OpenAI API to get a response for the prompt."""
        print("Processing with OpenAI...")
        
        # Call OpenAI API with a single prompt, no conversation history or batching
        try:
            response = self.client.responses.create(
                model=self.model_name,  # You can adjust the model as needed
                input=prompt,
                max_output_tokens=self.max_length,  # You can adjust this value depending on the output length
                temperature=self.temperature  # Adjust the temperature for randomness
            )
            # Extract the generated response from OpenAI's API response
            refactored_code = response.output[0].content[0].text
            #print(refactored_code)
            refactored_code = self.format_response(refactored_code)
            #print(refactored_code)
            return refactored_code
        
        except Exception as e:
            print(f"Error during OpenAI API call: {e} ")
            traceback.print_exc()
            sys.exit(1)  # Exit the program if there's an error
            return None

    def format_response(self, response):
        """Format the OpenAI response to remove markdown"""
        #the input is of type ```{languange} {code}```
        print("response before formatting:")
        print(response)
        response = response.split("\n")
        if response[0].startswith("```") and response[-1].endswith("```"):
            #remove the first line
            response = response[1:]
            #remove the last line
            response = response[:-1]
            #join the lines
        response = "\n".join(response)
        return response


@ResponseStrategyRegistry.register("gemini")
class GeminiResponse(ResponseStrategy):
    def __init__(self, model_name: str = "gemini-2.5-flash-preview-05-20", temperature: float = 1, max_length: int = 2048):
        super().__init__()
        self.client = genai.Client(api_key=gemini_api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_length = max_length
        
    def process(self, prompt):  
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=self.max_length,
                temperature=self.temperature,
            ),
        )

        return self.format_response(response.text) 
    
    def format_response(self, response):
        """Format the OpenAI response to remove markdown"""
        #the input is of type ```{languange} {code}```
        print("response before formatting:")
        print(response)
        response = response.split("\n")
        if response[0].startswith("```") and response[-1].endswith("```"):
            #remove the first line
            response = response[1:]
            #remove the last line
            response = response[:-1]
            #join the lines
        response = "\n".join(response)
        return response