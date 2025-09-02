"This file contains the routes for managing firewall rules in a Flask application"
from flask import Blueprint, request, jsonify
from flask_restx import Resource, Namespace, fields

from pydantic import TypeAdapter, ValidationError
from app.extensions import db
from app.models import Rule, Policy
from app.utils.common import safe_commit
from app.schemas.rule import ActionEnum, ProtocolEnum, RuleIn, RuleOut


ns = Namespace('rules', description='Rule operations')
REF_TEMPLATE = "#/definitions/{model}"
def to_out(rule: RuleOut) -> dict:
    """Convert a RuleOut model to a dictionary."""
    return {
        'id': rule.id,
        'source_ip': rule.source_ip,
        'destination_ip': rule.destination_ip,
        'protocol': rule.protocol,
        'action': rule.action,
        'port': rule.port
    }
ns.schema_model("ActionEnum",   TypeAdapter(ActionEnum).json_schema(ref_template=REF_TEMPLATE))
ns.schema_model("ProtocolEnum", TypeAdapter(ProtocolEnum).json_schema(ref_template=REF_TEMPLATE))


InSchema = ns.schema_model("RuleIn",  RuleIn.model_json_schema(ref_template=REF_TEMPLATE)) # Define the schema for the API request

@ns.route('/<int:policy_id>')
class RuleList(Resource):
    """Rules for a specific policy."""
    @ns.doc('list_rules')
    def get(self, policy_id: int) -> list:
        """List all rules for a specific policy."""
        rules = Rule.query.filter_by(policy_id=policy_id).all()
        return [to_out(r) for r in rules]

    @ns.expect(InSchema)
    def post(self, policy_id: int) -> dict:
        """Create a new rule for a specific policy."""
        try:
            dto = RuleIn.model_validate(request.get_json())
        except ValidationError as e:
            return {'errors': e.errors()}, 400

        policy = Policy.query.get(policy_id)
        if not policy:
            return {'errors': ['Policy not found']}, 404
        data = dto.model_dump(exclude={"id", "policy_id"})
        rule = Rule(**data, policy_id=policy_id)
        db.session.add(rule)

        if not safe_commit(db.session):
            return {'errors': ['Failed to create rule']}, 400
        return to_out(rule), 201


@ns.route('/<int:rule_id>')
class RuleDetail(Resource):
    """Details of a specific rule."""
    @ns.doc('delete_rule')
    def delete(self, rule_id: int) -> tuple:
        """Delete a specific rule."""
        rule = Rule.query.get(rule_id)
        if not rule:
            return {'errors': ['Rule not found']}, 404

        db.session.delete(rule)
        if not safe_commit(db.session):
            return {'errors': ['Failed to delete rule']}, 400
        return '', 204
