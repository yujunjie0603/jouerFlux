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
