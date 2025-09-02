"This file contains the routes for managing firewall policies in a Flask application"
import logging
from flask import Blueprint, request, jsonify
from flask_restx import Resource, Namespace, fields
from app import db
from app.models import Firewall, Policy
from app.utils.common import paginate_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ns = Namespace('firewall_policy', description='Firewall Policy operations')

@ns.route('/<int:firewall_id>/policy')
class FirewallPolicy(Resource):

    def post(self, firewall_id: int, policy_id: int) -> tuple:
        """Add a policy to a firewall.

        Args:
            firewall_id (int): The ID of the firewall.
            policy_id (int): The ID of the policy.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        firewall = Firewall.query.get_or_404(firewall_id)
        policy = Policy.query.get_or_404(policy_id)

        if policy in firewall.policies:
            return {'message': 'Policy already associated with firewall'}, 400

        firewall.policies.append(policy)
        db.session.commit()
        return {'message': 'Policy added to firewall'}, 200

    def delete(self, firewall_id: int, policy_id: int) -> tuple:
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
            return {'message': 'Policy not associated with firewall'}, 400

        firewall.policies.remove(policy)
        db.session.commit()
        return "", 204

    def get(self, firewall_id: int) -> tuple:
        """Get all policies associated with a firewall.

        Args:
            firewall_id (int): The ID of the firewall.

        Returns:
            tuple: A tuple containing the response data and status code.
        """
        firewall = Firewall.query.get_or_404(firewall_id)
        filters = []
        if firewall:
            filters.append(Policy.firewalls.any(id=firewall.id))

        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=25, type=int)
        except ValueError as e:
            logger.error(f"Invalid pagination parameters: {e}")
            return {'error': 'Invalid pagination parameters'}, 400
        paginated = paginate_query(Policy, filters=filters, page=page, per_page=per_page)
        results = [{'id': fw.id,
                    'name': fw.name,
                    'rules': [r.to_dict()
                              for r in fw.rules]}
                   for fw in paginated.items]

        return {
            'total': paginated.total,
            'pages': paginated.pages,
            'page': page,
            'per_page': per_page,
            'results': results
        }, 200
