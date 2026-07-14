"""Access control validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.lakehouse.models import RoleSpec, ValidationIssue


def load_access(path: Path) -> tuple[dict[str, RoleSpec], list[dict[str, Any]]]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    roles = {
        name: RoleSpec(
            name=name,
            description=str(spec.get("description", "")),
            layers=tuple(spec["layers"]),
            permissions=tuple(spec["permissions"]),
        )
        for name, spec in document["roles"].items()
    }
    return roles, list(document.get("policies", []))


def validate_access(roles: dict[str, RoleSpec]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if "analyst" in roles and "bronze" in roles["analyst"].layers:
        issues.append(
            ValidationIssue(
                severity="error",
                code="analyst_bronze_access",
                message="analyst role must not include bronze layer access",
            )
        )

    if "analyst" in roles and "write" in roles["analyst"].permissions:
        issues.append(
            ValidationIssue(
                severity="error",
                code="analyst_write_access",
                message="analyst role must be read-only",
            )
        )

    for role_name, role in roles.items():
        if "deploy" in role.permissions and role_name != "data_engineer":
            issues.append(
                ValidationIssue(
                    severity="warning",
                    code="deploy_permission",
                    message=f"{role_name} has deploy permission; prefer data_engineer only",
                )
            )

    return issues
