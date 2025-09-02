from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, field_validator
from typing import Annotated

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

IpPattern = Annotated[str, StringConstraints(
    min_length=7,
    max_length=64,
    pattern=r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
)]

class RuleIn(BaseModel):
    """Rule configuration for a network interface."""
    source_ip: IpPattern
    destination_ip: IpPattern
    protocol: ProtocolEnum
    action: ActionEnum
    port: int | None
    model_config = ConfigDict(from_attributes=True)

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

class RuleOut(BaseModel):
    """Rule configuration for a network interface."""
    id: int = Field(..., description="The unique identifier of the rule")
    source_ip: IpPattern
    destination_ip: IpPattern
    action: ActionEnum
    protocol: ProtocolEnum
    port: int | None
    model_config = ConfigDict(from_attributes=True)
