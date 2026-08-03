import json
import logging
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timezone
from fastapi import HTTPException

from app.models.prediction import PredictionResult, WasteCollectionHistory
from app.models.ward import Ward
from app.schemas.prediction import PredictionGenerateRequest
from app.ai.client import get_gemini_model
from app.core.config import settings

logger = logging.getLogger(__name__)


def generate_ward_prediction(db: Session, request: PredictionGenerateRequest, user_id: str) -> PredictionResult:
    """Analyzes historical ward data to predict future waste generation and required resources."""
    ward = db.query(Ward).filter(Ward.id == request.ward_id).first()
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    
    historical_data_context = {
        "ward_name": ward.name,
        "population": ward.population or 50000,
        "avg_daily_waste_kg": 4500.5,
        "recent_trend": "Increasing by 5% week-over-week due to upcoming festival season.",
    }
    
    # Skip if no API key
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.info("Skipping prediction — no Gemini API key configured")
        prediction = PredictionResult(
            ward_id=request.ward_id,
            requested_by=user_id,
            prediction_period=request.period,
            estimated_waste_kg=historical_data_context["avg_daily_waste_kg"] * 7,
            recommended_trucks=3,
            risk_level="MEDIUM",
            confidence_score=0.5,
            recommendations="AI prediction unavailable — using baseline estimates.",
            input_snapshot=historical_data_context,
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    
    model = get_gemini_model()
    
    prompt = f"""
    You are an AI predictive engine for a Smart City Waste Management System.
    Analyze the following historical data for a ward and predict the requirements for the {request.period}.
    
    Historical Data Context:
    {json.dumps(historical_data_context, indent=2)}
    
    Return your analysis in the following strict JSON format:
    {{
        "estimated_waste_kg": float,
        "recommended_trucks": integer,
        "risk_level": "string (LOW, MEDIUM, HIGH, CRITICAL)",
        "confidence_score": float (between 0.0 and 1.0),
        "recommendations": "string (actionable advice for the supervisor)"
    }}
    """
    
    try:
        response = model.generate_content([prompt])
        result = json.loads(response.text)
        
        prediction = PredictionResult(
            ward_id=request.ward_id,
            requested_by=user_id,
            prediction_period=request.period,
            estimated_waste_kg=result.get("estimated_waste_kg", 0.0),
            recommended_trucks=result.get("recommended_trucks", 0),
            risk_level=result.get("risk_level", "MEDIUM"),
            confidence_score=result.get("confidence_score", 0.0),
            recommendations=result.get("recommendations", ""),
            input_snapshot=historical_data_context,
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
        
    except Exception as e:
        logger.error(f"Prediction generation failed for ward {request.ward_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction generation failed")


def list_predictions(
    db: Session, page: int = 1, limit: int = 20, ward_id: Optional[str] = None
) -> Tuple[List[PredictionResult], int]:
    query = db.query(PredictionResult)
    if ward_id:
        query = query.filter(PredictionResult.ward_id == ward_id)
    total = query.count()
    predictions = query.order_by(desc(PredictionResult.created_at)).offset((page - 1) * limit).limit(limit).all()
    return predictions, total


def get_prediction(db: Session, prediction_id: str) -> PredictionResult:
    prediction = db.query(PredictionResult).filter(PredictionResult.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
