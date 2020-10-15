from dotenv import load_dotenv
load_dotenv()

import os
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
HOST_ADDRESS = os.getenv("HOST_ADDRESS")
HOST_PORT = int(os.getenv("HOST_PORT"))
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
