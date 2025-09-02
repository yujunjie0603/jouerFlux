from pydantic import BaseModel, Field, IPvAnyAddress, ConfigDict, StringConstraints
from typing import Optional, Annotated

NamePattern = Annotated[str, StringConstraints(
                        min_length=2,
                        max_length=100,
                        pattern=r'^[A-Za-z0-9_-]+$')]

class PolicyIn(BaseModel):
    """Policy configuration for a network interface."""
    model_config = ConfigDict(from_attributes=True)
    name: NamePattern

class PolicyOut(BaseModel):
    """Policy configuration for a network interface."""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="The unique identifier of the policy")
    name: NamePattern
