from tools.paths import resolve_work_path
from langchain.tools import tool

@tool
def read_file(path:str) -> str:
    """
    Reads a UTF-8 text file from the working directory.

    Args:
       path: Relative path of the file, e.g 'src/App.js' or 'README.md' or 'data/example.json'

    """
    
    try:
        file_path = resolve_work_path(path) # we are checking if the path is given to read is a valid path inside the working directory -> workspace or not 
    except ValueError as err:
     raise ValueError(f"path escapes working directory: {err}")


    try:
        return file_path.read_text(encoding="utf-8") # go and read the file 
    except FileNotFoundError as err:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError as err:
        raise PermissionError(f"Permission denied: {file_path}")
    except Exception as err:
        raise Exception(f"Error reading file: {file_path}")