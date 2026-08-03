import json
import logging
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.complaint import Complaint
from app.ai.client import get_gemini_model
from app.core.config import settings

logger = logging.getLogger(__name__)


def classify_complaint_image(db: Session, complaint_id: str, image_path: str = None) -> Complaint:
    """
    Sends the complaint details (and image if supported) to Gemini
    to extract structured metadata about the civic issue.
    Gracefully handles missing API key or API failures.
    """
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        return None

    # Skip AI classification if no API key configured
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.info(f"Skipping AI classification for {complaint_id} — no API key configured")
        return complaint

    try:
        model = get_gemini_model()
        
        prompt = f"""
        Analyze the following civic complaint regarding municipal waste/infrastructure.
        Title: {complaint.title}
        Description: {complaint.description or 'No description provided'}
        Category: {complaint.category}
        Location: lat={complaint.latitude}, lng={complaint.longitude}
        
        Based on the text, extract the following details in strict JSON format:
        {{
            "ai_waste_type": "string (e.g., Construction Debris, Organic, Mixed, Plastic)",
            "ai_severity": "integer between 1 and 10",
            "ai_suggested_category": "string (suggest a standardized category if current one seems wrong)",
            "ai_description": "string (a concise, objective summary of the issue)"
        }}
        """
        
        response = model.generate_content([prompt])
        result = json.loads(response.text)
        
        complaint.ai_waste_type = result.get("ai_waste_type")
        complaint.ai_severity = result.get("ai_severity")
        complaint.ai_suggested_category = result.get("ai_suggested_category")
        complaint.ai_description = result.get("ai_description")
        complaint.ai_classified_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(complaint)
        logger.info(f"Successfully classified complaint {complaint_id} via Gemini")
        
    except Exception as e:
        logger.error(f"Gemini classification failed for {complaint_id}: {str(e)}")
        # Graceful fallback: leave AI fields null and proceed
    
    return complaint
