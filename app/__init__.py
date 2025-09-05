"""This module initializes the Flask application and its extensions."""
from flask import Flask, redirect
from flask_cors import CORS
from app.extensions import db, migrate, api
from app.config import Config
import app.celery_app as celery_app
from .routes import firewalls, policies, rules, firewall_policy

def create_app():
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    api.add_namespace(firewalls.ns, path='/firewalls')
    api.add_namespace(policies.ns, path='/policies')
    api.add_namespace(rules.ns, path='/rules')
    api.add_namespace(firewall_policy.ns, path='/firewall_policys')
    app.url_map.strict_slashes = False
    celery_app.make_celery(app)

    # Redirect root URL to Swagger UI
    @app.route('/')
    def index():
        return redirect('/api/docs')

    return app
