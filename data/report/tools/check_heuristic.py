import os 


#check a heuristic on code (given as a string) and print if true or false
#the heuristic is a function that takes a string and returns a boolean
#check all the code in directories called refactored, but their parent directory is not called refactored_folder
#maybe i should put the option to multiple custom heuristics and their parameters, based on the name of the file

ROOTDIR = "../examples/"

def check_heuristic(heuristic, code):  
    """
    Check a heuristic on code (given as a string) and print if true or false.
    The heuristic is a function that takes a string and returns a boolean.
    Check all the code in directories called refactored, but their parent directory is not called refactored_folder.
    """
    #check if the heuristic is callable
    if not callable(heuristic):
        raise ValueError("Heuristic must be a callable function")
    
    #check if the code is a string
    if not isinstance(code, str):
        raise ValueError("Code must be a string")
    
    #check if the heuristic returns a boolean
    result = heuristic(code)
    if not isinstance(result, bool):
        raise ValueError("Heuristic must return a boolean")
    
    return result

def check_heuristic_in_directory(heuristic, directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip directories named 'refactored_folder'
        if 'refactored_folder' in dirpath:
            continue
        
        # Check if the directory is named 'refactored'
        if os.path.basename(dirpath) == 'refactored':
            for filename in filenames:
                if filename.endswith('.py') and not filename.startswith('__'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        code = file.read()
                        result = check_heuristic(heuristic, code)
                        print(f"File: {file_path}, Heuristic Result: {result}")


def number_of_classes(code, threshold=5):
    """
    Example heuristic: Check if the number of classes in the code is greater than 5.
    """
    return code.count('class ') > threshold


if __name__ == "__main__":
    
    heuristic = number_of_classes
    # Check the heuristic in the specified directory
    check_heuristic_in_directory(heuristic, ROOTDIR)