from dotenv import load_dotenv
load_dotenv()

import os
DATABASE_URL = os.getenv("DATABASE_URL")
HOST_ADDRESS = os.getenv("HOST_ADDRESS")
HOST_PORT = int(os.getenv("HOST_PORT"))
