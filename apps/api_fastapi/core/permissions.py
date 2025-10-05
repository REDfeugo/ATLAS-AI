"""Permission tier helpers for tool execution."""

from __future__ import annotations

from enum import Enum


class PermissionTier(str, Enum):
    """Supported permission tiers for tools."""

    FREE = "free"
    SAFE = "safe"
    ASK = "ask"
    NEVER = "never"


RISK_ESCALATION = {
    "low": PermissionTier.FREE,
    "medium": PermissionTier.SAFE,
    "high": PermissionTier.ASK,
}


def requires_confirmation(risk: str, tier: PermissionTier) -> bool:
    """Return True when the tool should request confirmation."""

    minimum = RISK_ESCALATION.get(risk, PermissionTier.FREE)
    if tier == PermissionTier.NEVER:
        return True
    if tier == PermissionTier.FREE:
        return minimum in {PermissionTier.SAFE, PermissionTier.ASK}
    if tier == PermissionTier.SAFE:
        return minimum == PermissionTier.ASK
    if tier == PermissionTier.ASK:
        return True
    return False
