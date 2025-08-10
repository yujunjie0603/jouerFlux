"""This module initializes the Flask application and its extensions."""
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS
from app.extensions import db, migrate
from app.swagger_config import template_swagger

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jouerflux.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'JouerFlux API',
        'uiversion': 3,
        'specs_route': '/apidocs'
    }

    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app, template=template_swagger)
    CORS(app)

    from .routes import firewalls, policies, rules, firewall_policy
    app.register_blueprint(firewalls.bp)
    app.register_blueprint(policies.bp)
    app.register_blueprint(rules.bp)
    app.register_blueprint(firewall_policy.bp)

    with app.app_context():
        db.create_all()

    # Redirect root URL to Swagger UI
    @app.route('/')
    def index():
        return redirect('/apidocs')

    return app
