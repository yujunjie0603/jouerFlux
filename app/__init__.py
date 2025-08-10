"""This module initializes the Flask application and its extensions."""
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS
from app.extensions import db, migrate
template = {
        "swagger": "2.0",
        "info": {
            "title": "JouerFlux API",
            "version": "1.0.0",
            "description": "Firewall management endpoints"
        },
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "definitions": {
            "Firewall": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"}
                }
            },
            "FirewallWithPolicies": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"},
                    "policies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id":   {"type": "integer"},
                                "name": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "Policy": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"},
                }
            },
            "Rule": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "action": {"type": "string"},
                    "source_ip": {"type": "string"},
                    "destination_ip": {"type": "string"},
                    "protocol": {"type": "string"},
                    "port": {"type": "integer"}
                }
            }
        }
    }

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
    Swagger(app, template=template)
    CORS(app)

    from .routes import firewalls, policies, rules, firewall_policy
    app.register_blueprint(firewalls.bp)
    app.register_blueprint(policies.bp)
    app.register_blueprint(rules.bp)
    app.register_blueprint(firewall_policy.bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return redirect('/apidocs')

    return app
