"This file contains the models for the firewall application"
from app.extensions import db
from app.utils.schema import ActionEnum, ProtocolEnum

firewall_policy = db.Table(
    'firewall_policy',
    db.Column('firewall_id', db.Integer, db.ForeignKey('firewall.id'), primary_key=True),
    db.Column('policy_id', db.Integer, db.ForeignKey('policy.id'), primary_key=True)
)


class Firewall(db.Model):
    """Model representing a firewall."""
    def __init__(self, name: str):
        self.name = name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_firewall_name'),
    )
    policies = db.relationship(
        'Policy',
        secondary=firewall_policy,
        back_populates='firewalls'
    )
    def __repr__(self):
        return f"<Firewall {self.name}>"


class Policy(db.Model):
    """Model representing a policy."""
    def __init__(self, name: str):
        self.name = name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rules = db.relationship('Rule', backref='policy', cascade="all, delete-orphan")
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_policy_name'),
    )
    firewalls = db.relationship(
        'Firewall',
        secondary=firewall_policy,
        back_populates='policies'
    )
    def __repr__(self):
        return f"<Policy {self.name}>"

class Rule(db.Model):
    """Model representing a firewall rule."""

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Enum(ActionEnum), nullable=False)
    protocol = db.Column(db.Enum(ProtocolEnum), nullable=False)
    source_ip = db.Column(db.String(45), nullable=False)
    destination_ip = db.Column(db.String(45), nullable=False)
    port = db.Column(db.Integer, nullable=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)

    def __repr__(self):
        return (f"<Rule {self.action.value.upper()} {self.protocol.value.upper()} "
                f"{self.source_ip} -> {self.destination_ip}:{self.port}>")

    def to_dict(self):
        """Convert the rule to a dictionary representation."""
        return {
            'id': self.id,
            'action': self.action.value,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'protocol': self.protocol.value,
            'port': self.port
        }
