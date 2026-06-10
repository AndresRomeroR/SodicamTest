import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(base_path, "../.env.dev")
        if os.path.exists(env_file):
            load_dotenv(env_file)

    def get(self, key: str):
        return os.getenv(key)
