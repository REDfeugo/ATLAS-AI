"""Promotion approval workflow routes."""

from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..logging_utils import append_log
from ..models import PromotionRequest, User
from ..security import get_current_user, require_admin

router = APIRouter()


@router.post("/request_promotion", response_model=schemas.PromotionRequestResponse)
def request_promotion(
    payload: schemas.PromotionRequestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> schemas.PromotionRequestResponse:
    """Create a promotion request entry."""

    req = PromotionRequest(
        requested_by=user.id,
        src_model=payload.src_model,
        src_version=payload.src_version,
        dst_model=payload.dst_model,
        notes=payload.notes,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    append_log("promotion_requested", user=user.email, path="/request_promotion", status="pending")
    return schemas.PromotionRequestResponse.model_validate(req)


@router.post("/approve_promotion", response_model=schemas.PromotionRequestResponse)
def approve_promotion(
    payload: schemas.PromotionApprovalRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> schemas.PromotionRequestResponse:
    """Approve a pending promotion request."""

    req = db.query(PromotionRequest).filter(PromotionRequest.id == payload.request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    req.status = "approved"
    req.approved_by = admin.id
    req.approved_at = dt.datetime.utcnow()
    db.add(req)
    db.commit()
    db.refresh(req)
    append_log("promotion_approved", user=admin.email, path="/approve_promotion", status="approved")
    return schemas.PromotionRequestResponse.model_validate(req)
