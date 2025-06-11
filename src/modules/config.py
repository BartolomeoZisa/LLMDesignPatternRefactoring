# config.py

#this is for the refactorer
PATTERNDESCRIPTIONPATH = "src/patterns/patternGOFjson"


#this is for the main
PROMPTFILE = "src/prompts/promptgeminixml.txt"
NUMITERATIONS = 1
SAVEFOLDERPATH = "geminiflash2.5_1"
FILETOREFACTOR = [] # if empty, all files in the match will be refactored
PROJECT_ROOT = "data/examples"
TEMPERATURE = 1
IGNOREHEADERS = []
#empty string means the default model
MODEL_NAME = "gemini-2.5-flash-preview-05-20" # or "gpt-4o-mini-2024-07-18"
MAX_LENGTH = 8192
STRATEGY = "gemini"  # or "gemini"