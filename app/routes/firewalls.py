"This module provides routes for managing firewalls in the JouerFlux application."
import logging
from flask import jsonify, request, Blueprint
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from flasgger.utils import swag_from
from app.models import Firewall
from app.extensions import db
import app.utils.common as common_utils
import app.schemas.firewall as firewall_schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ns = Namespace('firewalls', description='Firewall operations')

def to_out(row: firewall_schema.FirewallOut) -> dict:
    """Convert a Firewall model instance to a dictionary using Pydantic schema."""
    if not row:
        return {}
    return firewall_schema.FirewallOut.model_validate(row).model_dump()

InSchema  = ns.schema_model("FirewallIn", firewall_schema.FirewallIn.model_json_schema())
OutSchema = ns.schema_model("FirewallOut",    firewall_schema.FirewallOut.model_json_schema())

MAX_PER_PAGE = 100
@ns.route('/')
class FirewallList(Resource):
    """Endpoint for listing and creating firewalls."""

    @ns.param("page", "page (>=1), default 1", _in='query', type='integer')
    def get(self):
        """List all firewalls."""

        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=25, type=int)
        except ValueError as e:
            logger.error(f"Invalid pagination parameters: {e}")
            return {'error': 'Invalid pagination parameters'}, 400

        filters = []
        if 'name' in request.args:
            name = request.args.get("name")
            filters.append(Firewall.name.ilike(f"%{name}%"))

        paginated = common_utils.paginate_query(Firewall, filters=filters, page=page, per_page=per_page)
        results = [to_out(row) for row in paginated.items]
        return {
            'total': paginated.total,
            'pages': paginated.pages,
            'page': page,
            'per_page': per_page,
            'results': results
        }, 200

    @ns.expect(InSchema)
    def post(self):
        """Create a new firewall."""
        data = request.json
        try:
            dto = firewall_schema.FirewallIn.model_validate(data)
        except ValidationError as e:
            return {'error': str(e)}, 400

        firewall = Firewall(name=dto.name)
        db.session.add(firewall)

        if not common_utils.safe_commit(db.session):
            return {'error': 'Failed to create firewall'}, 500


        return to_out(firewall), 201

@ns.route('/<int:firewall_id>')
class FirewallDetail(Resource):
    """Endpoint for retrieving, updating, and deleting a specific firewall."""

    def get(self, firewall_id: int):
        """Get a specific firewall by ID."""
        firewall = Firewall.query.get_or_404(firewall_id)
        return to_out(firewall), 200

    def delete(self, firewall_id: int):
        """Delete a specific firewall by ID."""
        firewall = Firewall.query.get_or_404(firewall_id)
        db.session.delete(firewall)

        if not common_utils.safe_commit(db.session):
            return {'error': 'Failed to delete firewall'}, 500

        return "", 204
