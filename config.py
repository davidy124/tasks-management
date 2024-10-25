import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URI', 'mongodb://mongo:27017/tasks_manager'),
        'username': os.getenv('MONGODB_USERNAME', 'root'),
        'password': os.getenv('MONGODB_PASSWORD', 'password'),
        'authentication_source': 'admin',
        'connect': True,
    }

    # Add other configuration variables as needed
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
