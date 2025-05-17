import os
from abc import ABC, abstractmethod
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")



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
        return len(response.split(" "))

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
        


class OpenAIResponse(ResponseStrategy):

    def __init__(self, model_name: str = "gpt-4o-mini-2024-07-18", temperature: float = 1, max_length: int = 2048):
        super().__init__()
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)


    def process(self, prompt):
        """Use the OpenAI API to get a response for the prompt."""
        print("Processing with OpenAI...")
        
        # Call OpenAI API with a single prompt, no conversation history or batching
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,  # You can adjust the model as needed
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_length,  # You can adjust this value depending on the output length
                temperature=self.temperature  # Adjust the temperature for randomness
            )
            # Extract the generated response from OpenAI's API response
            refactored_code = response.choices[0].message.content
            #print(refactored_code)
            refactored_code = self.format_response(refactored_code)
            #print(refactored_code)
            return refactored_code
        
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

    def format_response(self, response):
        """Format the OpenAI response to remove markdown"""
        #the input is of type ```{languange} {code}```
        response = response.split("\n")
        #remove the first line
        response = response[1:]
        #remove the last line
        response = response[:-1]
        #join the lines
        response = "\n".join(response)
        return response
