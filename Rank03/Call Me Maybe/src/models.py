"""Data models for function calling definitions, tests, and outputs."""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class ParameterProperty(BaseModel):
    """Schema definition for an individual function parameter."""

    model_config = ConfigDict(extra="ignore")

    type: str = Field(..., description="Data type: string, number, boolean")
    description: str | None = Field(default=None)


class ReturnProperty(BaseModel):
    """Schema definition for the function return type."""

    model_config = ConfigDict(extra="ignore")

    type: str


class FunctionDefinition(BaseModel):
    """Schema definition for an available tool function."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str
    parameters: dict[str, ParameterProperty] = Field(default_factory=dict)
    returns: ReturnProperty | None = Field(default=None)


class TestCase(BaseModel):
    """Test input case containing a natural language prompt."""

    model_config = ConfigDict(extra="ignore")

    prompt: str


class FunctionCallResult(BaseModel):
    """Final formatted output item for a processed prompt."""

    model_config = ConfigDict(extra="ignore")

    prompt: str
    name: str
    parameters: dict[str, Any]


class AppConfig(BaseModel):
    """Command line and runtime configuration."""

    model_config = ConfigDict(extra="ignore")

    functions_path: str = "data/input/functions_definition.json"
    input_path: str = "data/input/function_calling_tests.json"
    output_path: str = "data/output/function_calling_results.json"
