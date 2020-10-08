from dotenv import load_dotenv
load_dotenv()

import os
HOST_ADDRESS = os.getenv("HOST_ADDRESS")
HOST_PORT = int(os.getenv("HOST_PORT"))
