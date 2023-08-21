import os
from dotenv import load_dotenv

# Read the parameters from the .env file and return them
def readConnectionParametersEnv():
    load_dotenv()
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    sid = os.getenv('SID')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    return host, port, sid, user, password