"This module provides routes for managing firewalls in the JouerFlux application."
import logging
from flask import jsonify, request, Blueprint
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from flasgger.utils import swag_from
from app.models import Firewall
from app.extensions import db
import app.utils.common as common_utils
from app.utils.schema import NameCheck

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('firewalls', __name__, url_prefix='/firewalls')

@swag_from('/app/swagger/firewall/get_list.yaml', methods=['get'])
@bp.route('/', methods=['GET'])
def list_firewalls()-> tuple:
    """List all firewalls.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    logger.info("Fetching all firewalls")
    try :
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
    except ValueError as e:
        logger.error(f"Invalid pagination parameters: {e}")
        return jsonify({'error': 'Invalid pagination parameters'}), 400
    filters = []
    name = request.args.get('name', default=None, type=str)
    if name:
        filters.append(Firewall.name.ilike(f"%{name}%"))
    paginated = common_utils.paginate_query(Firewall, filters=filters, page=page, per_page=per_page)
    results = [{'id': fw.id, 'name': fw.name} for fw in paginated.items]
    return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'page': page,
            'per_page': per_page,
            'results': results
        }), 200

@swag_from('/app/swagger/firewall/get_by_id.yaml', methods=['get'])
@bp.route('/<int:firewall_id>', methods=['GET'])
def get_firewall(firewall_id: int) -> tuple:
    """Get a specific firewall by ID.
    Args:
        firewall_id (int): The ID of the firewall.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    logger.info(f"Fetching firewall with ID: {firewall_id}")
    firewall = Firewall.query.get_or_404(firewall_id)
    return jsonify({
        'id': firewall.id,
        'name': firewall.name,
        'policies': [{'id': p.id, 'name': p.name} for p in firewall.policies]
    }), 200


@swag_from('/app/swagger/firewall/post.yaml', methods=['post'])
@bp.route('', methods=['POST'])
def create_firewall()->tuple:
    """Create a new firewall.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    logger.info(f"Creating firewall with data {request.json}")
    data = request.json
    # Check name value
    try:
        dto = NameCheck.model_validate(data)

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400

    existing = Firewall.query.filter_by(name=dto.name).first()
    if existing:
        logger.warning(f"Firewall with name {dto.name} already exists.")
        return jsonify({"error": "Firewall with this name already exists."}), 400

    firewall = Firewall(name=dto.name)
    db.session.add(firewall)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Error creating firewall: {e}")
        return jsonify({"error": "Failed to create firewall. This name is already taken."}), 500

    return jsonify({'id': firewall.id, 'name': firewall.name}), 201


@swag_from('/app/swagger/firewall/delete.yaml', methods=['delete'])
@bp.route('/<int:firewall_id>', methods=['DELETE'])
def delete_firewall(firewall_id: int) -> tuple:
    """Delete a firewall by ID.

    Args:
        id (int): The ID of the firewall to delete.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    firewall = Firewall.query.get_or_404(firewall_id)
    db.session.delete(firewall)
    db.session.commit()

    return f'Firewall {firewall.name} ({firewall.id}) deleted', 200
