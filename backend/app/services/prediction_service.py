import json
import logging
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.prediction import PredictionResult, WasteCollectionHistory
from app.models.ward import Ward
from app.schemas.prediction import PredictionGenerateRequest
from app.ai.client import get_gemini_model

logger = logging.getLogger(__name__)

def generate_ward_prediction(db: Session, request: PredictionGenerateRequest, user_id: str) -> PredictionResult:
    """
    Analyzes historical ward data to predict future waste generation and required resources.
    """
    ward = db.query(Ward).filter(Ward.id == request.ward_id).first()
    
    # In a production app, we would query `WasteCollectionHistory` for the last 30 days.
    # For this MVP, we will simulate the historical context sent to the LLM.
    historical_data_context = {
        "ward_name": ward.name if ward else "Unknown Ward",
        "population": ward.population if ward else 50000,
        "avg_daily_waste_kg": 4500.5,
        "recent_trend": "Increasing by 5% week-over-week due to upcoming festival season."
    }
    
    model = get_gemini_model()
    
    prompt = f"""
    You are an AI predictive engine for a Smart City Waste Management System.
    Analyze the following historical data for a ward and predict the requirements for the {request.period}.
    
    Historical Data Context:
    {json.dumps(historical_data_context, indent=2)}
    
    Return your analysis in the following strict JSON format:
    {{
        "estimated_waste_kg": float (predicted waste),
        "recommended_trucks": integer (number of trucks needed),
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
            input_snapshot=historical_data_context
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
        
    except Exception as e:
        logger.error(f"Prediction generation failed for ward {request.ward_id}: {str(e)}")
        raise e
