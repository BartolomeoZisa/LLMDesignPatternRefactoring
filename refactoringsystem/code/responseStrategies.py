import os
from abc import ABC, abstractmethod
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")



class ResponseStrategy(ABC):

    @abstractmethod
    def process(self, prompt): 
        """Process the prompt and return a response."""
        pass
    def length(self, response):
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

    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)


    def process(self, prompt):
        """Use the OpenAI API to get a response for the prompt."""
        print("Processing with OpenAI...")
        
        # Call OpenAI API with a single prompt, no conversation history or batching
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # You can adjust the model as needed
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000  # You can adjust this value depending on the output length
            )
            # Extract the generated response from OpenAI's API response
            refactored_code = response.choices[0].message.content
            return refactored_code
        
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

