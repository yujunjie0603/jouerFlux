"This file contains the Pydantic models for firewall rules in a Flask application"
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, IPvAnyAddress, field_validator, StringConstraints

class ActionEnum(str, Enum):
    """Enumeration for action types in firewall rules."""
    ALLOW = 'ALLOW'
    DENY = 'DENY'

class ProtocolEnum(str, Enum):
    """Enumeration for protocol types in firewall rules."""
    TCP = 'TCP'
    UDP = 'UDP'
    ICMP = 'ICMP'
    GRE = 'GRE'
    ESP = 'ESP'
    AH = 'AH'
    ALL = 'ALL'

class RuleCheck(BaseModel):
    """Pydantic model for firewall rules."""
    action: ActionEnum
    protocol: ProtocolEnum
    source_ip: IPvAnyAddress
    destination_ip: IPvAnyAddress
    port: int | None = None

    @field_validator('port')
    @classmethod
    def validate_port(cls, value, info):
        """Validate that the port is within the valid range."""
        proto = info.data.get('protocol')
        if proto in {ProtocolEnum.TCP, ProtocolEnum.UDP}:
            # Port must be specified for TCP/UDP protocols
            if value is None or not 0 <= value <= 65535:
                raise ValueError('Port must be specified for TCP/UDP protocols')

        elif value is not None:
            raise ValueError('Port must be None for non-TCP/UDP protocols')

        return value

NamePattern = Annotated[str, StringConstraints(min_length=1,
                                               max_length=100,
                                               pattern=r'^[A-Za-z0-9_-]+$')]
class NameCheck(BaseModel):
    """Pydantic model for validating names."""
    name: NamePattern

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        """Validate that the name is not empty and matches the pattern."""
        if not value:
            raise ValueError('Name cannot be empty')
        return value
