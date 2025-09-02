"""Manage firewall policies and routes for the JouerFlux application."""
import logging
from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError
from flasgger.utils import swag_from
from app.extensions import db
from app.models import Policy
from app.utils.common import paginate_query, safe_commit, paginate_to_dict
from app.schemas.policy import PolicyIn, PolicyOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ns = Namespace('policies', description='Policy operations')

def to_out(policy: PolicyOut) -> dict:
    """Convert a Policy model instance to a dictionary using Pydantic schema."""
    if not policy:
        return {}
    return PolicyOut.model_validate(policy).model_dump()

InSchema  = ns.schema_model("PolicyIn",  PolicyIn.model_json_schema())

parser_get_list = ns.parser()
parser_get_list.add_argument("page", type=int, required=False, default=1, help="Page number (>=1)")
parser_get_list.add_argument("per_page", type=int, required=False, default=1, help="Number of items per page")
parser_get_list.add_argument("name", type=str, required=False, help="Name of the policy")

@ns.route('/')
class PolicyList(Resource):
    """Manage policies.

    Args:
        Resource (flask_restx.Resource): The base resource class.
    """
    @ns.expect(parser_get_list)
    def get(self):
        """Get a list of all policies."""
        args = parser_get_list.parse_args()
        page = args.get("page", 1)
        per_page = args.get("per_page", 1)
        name = args.get("name")

        filters = []
        if name:
            filters.append(Policy.name.ilike(f"%{name}%"))

        paginated = paginate_query(Policy, filters=filters, page=page, per_page=per_page)

        results = [to_out(policy) for policy in paginated.items]
        return paginate_to_dict(paginated, results), 200

    @ns.expect(InSchema) # an example of request body with expect model
    def post(self):
        """Create a new policy."""
        try:
            policy_data = PolicyIn.model_validate(request.json)
            new_policy = Policy(**policy_data)  # Assuming firewall_id is available
            db.session.add(new_policy)
            if not safe_commit(db.session):
                return jsonify({"error": "Failed to create policy"}), 500
            return jsonify(to_out(new_policy)), 201

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return jsonify({"error": e.errors()}), 400

@ns.route('/<int:policy_id>')
class PolicyDetail(Resource):
    """Manage a specific policy.

    Args:
        Resource (flask_restx.Resource): The base resource class.
    """
    @ns.doc(responses={200: 'Success', 404: 'Policy not found'})
    @ns.param('policy_id', 'The policy ID', type='integer')
    def get(self, policy_id):
        """Get a policy by ID.

        Args:
            policy_id (int): The ID of the policy.

        Returns:
            dict: The policy data or an error message.
        """
        policy = Policy.query.get(policy_id)
        if not policy:
            return {"error": "Policy not found"}, 404
        return to_out(policy), 200


    def delete(self, policy_id):
        """delete a policy by ID.

        Args:
            policy_id (int): The ID of the policy.

        Returns:
            dict: The policy data or an error message.
        """
        policy = Policy.query.get(policy_id)
        if not policy:
            return {"error": "Policy not found"}, 404
        db.session.delete(policy)
        if not safe_commit(db.session):
            return {"error": "Failed to delete policy"}, 500
        return {"message": "Policy deleted"}, 204
