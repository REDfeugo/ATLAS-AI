"""Audit log utilities for tool execution."""

from __future__ import annotations

import json
from typing import Dict, List

from sqlalchemy.orm import Session

from ..core import models


class AuditService:
    """Persist tool execution details for accountability."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def record_event(
        self,
        tool_name: str,
        args: Dict[str, object],
        result_summary: str,
        risk_level: str,
        confirmation_token: str | None,
        succeeded: bool = True,
    ) -> int:
        """Store an audit event and return its identifier."""

        event = models.AuditEvent(
            tool_name=tool_name,
            args_json=json.dumps(args),
            result_summary=result_summary,
            risk_level=risk_level,
            confirmation_token=confirmation_token,
            succeeded=succeeded,
        )
        self.session.add(event)
        self.session.flush()
        return event.id

    def list_events(self) -> List[models.AuditEvent]:
        """Return the most recent audit events."""

        stmt = self.session.query(models.AuditEvent).order_by(models.AuditEvent.id.desc()).limit(50)
        return list(stmt)
