"This file contains the routes for managing firewall rules in a Flask application"
from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from app.extensions import db
from app.models import ActionEnum, ProtocolEnum, Rule, Policy
from app.utils.common import safe_commit, validate_enum, validate_ip, validate_port

bp = Blueprint('rules', __name__, url_prefix='/rules')

@swag_from('/app/swagger/rule/get_by_policy.yaml', methods=['get'])
@bp.route('/policy/<int:policy_id>', methods=['GET'])
def list_rules(policy_id: int) -> tuple:
    """List all rules for a specific policy.
    Args:
        policy_id (int): The ID of the policy for which to list rules.
    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    rules = Rule.query.filter_by(policy_id=policy_id).all()
    return jsonify([
        r.to_dict() for r in rules
    ])

@swag_from('/app/swagger/rule/post.yaml', methods=['post'])
@bp.route('/policy/<int:policy_id>', methods=['POST'])
def create_rule(policy_id: int) -> tuple:
    """Create a new rule for a specific policy.
    Args:
        policy_id (int): The ID of the policy to which the rule will be added.
    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    data = request.json
    policy = Policy.query.get_or_404(policy_id)
    str_action = data.get('action', '').upper() if data.get('action') else None
    str_protocol = data.get('protocol', '').upper() if data.get('protocol') else None

    try:
        action = validate_enum(str_action, ActionEnum)
        protocol = validate_enum(str_protocol, ProtocolEnum)
        port = validate_port(int(data.get('port')))
        source_ip = validate_ip(data.get('source_ip'))
        destination_ip = validate_ip(data.get('destination_ip'))

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    rule = Rule(
        action=action,
        protocol=protocol,
        source_ip=source_ip,
        destination_ip=destination_ip,
        port=port,
        policy=policy
    )
    db.session.add(rule)

    if not safe_commit(db.session):
        return jsonify({'error': 'Failed to create rule'}), 500

    return jsonify(rule.to_dict()), 201

@swag_from('/app/swagger/rule/delete.yaml', methods=['delete'])
@bp.route('/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id: int) -> tuple:
    """Delete a rule by ID.
    Args:
        rule_id (int): The ID of the rule to delete.
    Returns:
        tuple: A tuple containing the HTTP status code.
    """
    rule = Rule.query.get_or_404(rule_id)
    db.session.delete(rule)
    if not safe_commit(db.session):
        return jsonify({'error': 'Failed to delete rule'}), 500
    return '', 204
