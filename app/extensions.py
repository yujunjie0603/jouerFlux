"This file contains the extensions for the Flask application"
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

api = Api(
    title="Firewall API",
    version="1.0",
    description="A simple API for managing firewall rules",
    doc="/api/docs",
    #validate=True,
)

db = SQLAlchemy()
migrate = Migrate()
