import os
from dotenv import load_dotenv

load_dotenv()

MAX_NUMBER_OF_SATELLITES = int(os.environ.get('MAX_NUMBER_OF_SATELLITES', 4))

TCP_IP = os.environ.get('TCP_IP', "localhost")
TCP_PORT = int(os.environ.get('TCP_PORT', 8888))
BUFFER_SIZE = int(os.environ.get('BUFFER_SIZE', 1024))
FULL_SCREEN = int(os.environ.get('FULL_SCREEN', 0))

RED        = os.environ.get('RED',        "235;52;52")
GREEN      = os.environ.get('GREEN',      "52;235;52")
BLUE       = os.environ.get('BLUE',       "52;52;235")
YELLOW     = os.environ.get('YELLOW',     "235;235;52")
LIGHT_BLUE = os.environ.get('LIGHT_BLUE', "52;235;235")
PINK       = os.environ.get('PINK',       "235;52;235")
WHITE      = os.environ.get('WHITE',      "235;235;23")
