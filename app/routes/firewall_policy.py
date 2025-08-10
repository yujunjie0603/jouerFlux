"This file contains the routes for managing firewall policies in a Flask application"
import logging
from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from app import db
from app.models import Firewall, Policy
from app.utils.common import paginate_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('firewall_policy', __name__, url_prefix='/firewall-policy')

@swag_from('/app/swagger/firewall_policy/add_to_firewall.yaml', methods=['post'])
@bp.route('/<int:firewall_id>/add/<int:policy_id>', methods=['POST'])
def add_policy_to_firewall(firewall_id: int, policy_id: int) -> tuple:
    """_summary_

    Args:
        firewall_id (int): _description_
        policy_id (int): _description_

    Returns:
        tuple: _description_
    """
    firewall = Firewall.query.get_or_404(firewall_id)
    policy = Policy.query.get_or_404(policy_id)

    if policy in firewall.policies:
        return jsonify({'message': 'Policy already associated with firewall'}), 400

    firewall.policies.append(policy)
    db.session.commit()
    return jsonify({'message': 'Policy added to firewall'}), 200

@swag_from('/app/swagger/firewall_policy/remove_from_firewall.yaml', methods=['delete'])
@bp.route('/<int:firewall_id>/remove/<int:policy_id>', methods=['DELETE'])
def remove_policy_from_firewall(firewall_id: int, policy_id: int) -> tuple:
    """Remove a policy from a firewall.

    Args:
        firewall_id (int): The ID of the firewall.
        policy_id (int): The ID of the policy.

    Returns:
        tuple: A tuple containing the response data and status code.
    """
    firewall = Firewall.query.get_or_404(firewall_id)
    policy = Policy.query.get_or_404(policy_id)

    if policy not in firewall.policies:
        return jsonify({'message': 'Policy not associated with firewall'}), 400

    firewall.policies.remove(policy)
    db.session.commit()
    return "", 204

@swag_from('/app/swagger/firewall_policy/get_by_firewall.yaml', methods=['get'])
@bp.route('/<int:firewall_id>/policies', methods=['GET'])
def get_policies_of_firewall(firewall_id: int) -> tuple :
    """_summary_

    Args:
        firewall_id (int): _description_

    Returns:
        tuple: _description_
    """
    firewall = Firewall.query.get_or_404(firewall_id)
    filters = []
    if firewall:
        filters.append(Policy.firewalls.any(id=firewall.id))

    try :
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=25, type=int)
    except ValueError as e:
        logger.error(f"Invalid pagination parameters: {e}")
        return jsonify({'error': 'Invalid pagination parameters'}), 400
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
