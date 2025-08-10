"""Manage firewall policies and routes for the JouerFlux application."""
import logging
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from flasgger.utils import swag_from
from app.extensions import db
from app.models import Policy
from app.utils.common import paginate_query, safe_commit
from app.utils.schema import NameCheck

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('policies', __name__, url_prefix='/policies')

@swag_from('/app/swagger/policy/get_list.yaml', methods=['get'])
@bp.route('/', methods=['GET'])
def list_all_policies()-> tuple:
    """List all firewall policies.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    try :
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=25, type=int)
    except ValueError as e:
        logger.error(f"Invalid pagination parameters: {e}")
        return jsonify({'error': 'Invalid pagination parameters'}), 400
    filters = []
    name = request.args.get('name', default=None, type=str)
    if name:
        filters.append(Policy.name.ilike(f"%{name}%"))

    paginated = paginate_query(Policy, filters=filters, page=page, per_page=per_page)
    results = [{'id': fw.id,
                'name': fw.name, 
                'rules': [r.to_dict() 
                          for r in fw.rules]}
               for fw in paginated.items]

    return jsonify({
        'total': paginated.total,
        'pages': paginated.pages,
        'page': page,
        'per_page': per_page,
        'results': results
    }), 200

@swag_from('/app/swagger/policy/get_by_id.yaml', methods=['get'])
@bp.route('/<int:policy_id>', methods=['GET'])
def list_policies(policy_id: int) -> tuple:
    """List a specific policy by ID.
    Args:
        policy_id (int): The ID of the policy to retrieve.
    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    policies = Policy.query.get_or_404(policy_id)
    return jsonify({
        'id': policies.id,
        'name': policies.name,
        'rules': [r.to_dict() for r in policies.rules]
    })

@swag_from('/app/swagger/policy/post.yaml', methods=['post'])
@bp.route('/', methods=['POST'])
def create_policy() -> tuple:
    """Create a new firewall policy.
    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    data = request.json
    # Check name value
    try:
        dto = NameCheck.model_validate(data)

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400

    existing = Policy.query.filter_by(name=dto.name).first()
    if existing:
        return jsonify({"error": "Policy with this name already exists."}), 400

    policy = Policy(name=dto.name)
    db.session.add(policy)

    if not safe_commit(db.session):
        logger.error("Failed to create policy")
        return jsonify({'error': 'Failed to create policy'}), 500

    return jsonify({'id': policy.id, 'name': policy.name}), 201

@swag_from('/app/swagger/policy/delete.yaml', methods=['delete'])
@bp.route('/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id: int) -> tuple:
    """Delete a policy by ID.
    Args:
        policy_id (int): The ID of the policy to delete.
    Returns:
        tuple: A tuple containing the HTTP status code.
    """
    policy = Policy.query.get_or_404(policy_id)
    db.session.delete(policy)

    if not safe_commit(db.session):
        return jsonify({'error': 'Failed to delete policy'}), 500

    return '', 204
