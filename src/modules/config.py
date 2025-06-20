# config.py

#this is for the main

NUMITERATIONS = 1
SAVEFOLDERPATH ="prova" #"prova_1" #
FILETOREFACTOR = [] # if empty, all files in the match will be refactored
PROJECT_ROOT = "data/examples"
TEMPERATURE = 1
IGNOREHEADERS = []
#empty string means the default model
MODEL_NAME = "gpt-4o-2024-08-06" #"gpt-4o-mini-2024-07-18"
 # or  "gemini-2.5-flash-preview-05-20" 
MAX_LENGTH = 8192
STRATEGY = "openai"  #openai or "gemini"