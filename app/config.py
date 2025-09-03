"Configuration for the Flask application and Swagger API documentation"
import os

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///jouerflux.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SWAGGER = {
        'title': 'JouerFlux API',
        'uiversion': 3,
        'specs_route': '/apidocs'
    }
    
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
    CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true"
    TIMEZONE = os.getenv("TIMEZONE", "Europe/Paris")

    EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://example.com/notify/firewall")
    EXTERNAL_API_TOKEN = os.getenv("EXTERNAL_API_TOKEN", "secret_token")  