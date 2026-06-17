from __future__ import annotations

from pathlib import Path

import yaml

from .models import AgentDef, WarPackage


def load_agent(path: str | Path) -> AgentDef:
    return AgentDef.model_validate(yaml.safe_load(Path(path).read_text()))


def load_package(dir_path: str | Path) -> WarPackage:
    p = Path(dir_path) / "package.yaml"
    return WarPackage.model_validate(yaml.safe_load(p.read_text()))
