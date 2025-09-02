from pydantic import BaseModel, Field, IPvAnyAddress, ConfigDict, StringConstraints
from typing import Optional, Annotated

NamePattern = Annotated[str, StringConstraints(
                        min_length=4,
                        max_length=100,
                        pattern=r'^[A-Za-z0-9_-]+$')]

class FirewallIn(BaseModel):
    """Firewall configuration for a network interface."""
    model_config = ConfigDict(from_attributes=True)
    name: NamePattern

class FirewallOut(BaseModel):
    """Firewall configuration for a network interface."""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="The unique identifier of the firewall")
    name: NamePattern
