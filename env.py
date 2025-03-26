import os
from dotenv import load_dotenv

load_dotenv()

def get(key = None):
    if key == None:
        return os.environ
    
    return os.environ[key]
