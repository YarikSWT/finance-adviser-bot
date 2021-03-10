import os

RUNNING_ADDRESS = os.getenv("RUNNING_ADDRESS", "0.0.0.0")
PORT = int(os.environ.get('PORT', '8000'))