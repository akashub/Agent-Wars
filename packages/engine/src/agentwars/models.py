from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

LAYERS = ("persona", "tools", "memory", "strategy", "sub_agents", "model")


class LayerRule(BaseModel):
    frozen: bool = False
    value: object | None = None
    token_cap: int | None = None
    max_tools: int | None = None


class Budget(BaseModel):
    max_tokens: int
    max_tool_calls: int
    wall_clock_seconds: int


class Ruleset(BaseModel):
    layers: dict[str, LayerRule]
    budget: Budget
    runs_per_agent: int = 1
    seed_policy: str = "fixed_per_run"

    @field_validator("layers")
    @classmethod
    def _known_layers(cls, v: dict[str, LayerRule]) -> dict[str, LayerRule]:
        unknown = set(v) - set(LAYERS)
        if unknown:
            raise ValueError(f"unknown layers: {sorted(unknown)}")
        return v


class Scoring(BaseModel):
    base_points: float = 100.0
    tiebreakers: list[str] = Field(default_factory=lambda: ["fewest_tokens", "fastest"])


class TaskSpec(BaseModel):
    visibility: str = "sealed"
    baseline_path: str
    grader_path: str


class AgentDef(BaseModel):
    id: str
    name: str
    architect: str
    model: str
    persona: str = ""
    tools: list[str] = Field(default_factory=list)
    memory: dict = Field(default_factory=dict)
    strategy: dict = Field(default_factory=dict)
    sub_agents: list[dict] = Field(default_factory=list)
    cosmetics: dict = Field(default_factory=dict)

    @field_validator("architect")
    @classmethod
    def _architect_set(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("architect must be set")
        return v


class WarPackage(BaseModel):
    id: str
    name: str
    format: str
    author: str
    task: TaskSpec
    ruleset: Ruleset
    scoring: Scoring = Field(default_factory=Scoring)
