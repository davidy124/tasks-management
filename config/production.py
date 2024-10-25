from .base import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
    # Add any production-specific configurations here
    # For example, you might want to set MONGODB_SETTINGS to use a different database
