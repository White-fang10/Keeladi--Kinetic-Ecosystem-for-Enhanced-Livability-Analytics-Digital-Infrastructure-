from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.db.session import get_db
from app.schemas.prediction import PredictionGenerateRequest, PredictionResultResponse
from app.schemas.core import StandardResponse, Pagination
from app.services.prediction_service import generate_ward_prediction, list_predictions, get_prediction
from app.api.deps import require_supervisor

router = APIRouter()


@router.post("/generate", response_model=StandardResponse[PredictionResultResponse])
def generate_prediction(
    request: PredictionGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Generate ward prediction using Gemini AI (Admin/Supervisor only)."""
    prediction = generate_ward_prediction(db, request, current_user.id)
    return StandardResponse(success=True, message="Prediction generated", data=prediction)


@router.get("", response_model=StandardResponse[List[PredictionResultResponse]])
def get_all_predictions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    ward_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """List past predictions with optional ward filter."""
    predictions, total = list_predictions(db, page=page, limit=limit, ward_id=ward_id)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=predictions, pagination=pagination)


@router.get("/{prediction_id}", response_model=StandardResponse[PredictionResultResponse])
def read_prediction(
    prediction_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get specific prediction detail."""
    prediction = get_prediction(db, prediction_id)
    return StandardResponse(success=True, data=prediction)
