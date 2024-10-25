import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/tasks_manager'),
        'username': os.getenv('MONGODB_USERNAME'),
        'password': os.getenv('MONGODB_PASSWORD'),
        'authentication_source': 'admin',
        'connect': False,
    }
