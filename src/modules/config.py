# config.py

#this is for the refactorer
PATTERNDESCRIPTIONPATH = "src/patterns/patternGOFjson"


#this is for the main
PROMPTFILE = "src/prompts/promptgeminixml.txt"
NUMITERATIONS = 3
SAVEFOLDERPATH = "prova_1" #"gpt4.0_1"
FILETOREFACTOR = [] # if empty, all files in the match will be refactored
PROJECT_ROOT = "data/examples"
TEMPERATURE = 1
IGNOREHEADERS = []
#empty string means the default model
MODEL_NAME = "gpt-4o-mini-2024-07-18"
 # or  "gemini-2.5-flash-preview-05-20" "gpt-4o-2024-08-06"
MAX_LENGTH = 8192
STRATEGY = "openai"  #openai or "gemini"