import json
import logging
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.complaint import Complaint
from app.ai.client import get_gemini_model

logger = logging.getLogger(__name__)

def classify_complaint_image(db: Session, complaint_id: str, image_path: str = None) -> Complaint:
    """
    Sends the complaint details (and image if supported) to Gemini 
    to extract structured metadata about the civic issue.
    """
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        return None

    model = get_gemini_model()
    
    prompt = f"""
    Analyze the following civic complaint regarding municipal waste/infrastructure.
    Title: {complaint.title}
    Description: {complaint.description or 'No description provided'}
    Category: {complaint.category}
    
    Based on the text (and the provided image context if applicable), extract the following details in strict JSON format:
    {{
        "ai_waste_type": "string (e.g., Construction Debris, Organic, Mixed, Plastic)",
        "ai_severity": "integer between 1 and 10",
        "ai_suggested_category": "string (suggest a standardized category if current one seems wrong)",
        "ai_description": "string (a concise, objective summary of the issue)"
    }}
    """
    
    try:
        # Note: In a real implementation with an actual image file, 
        # we would upload it using genai.upload_file() and pass it in the array.
        # For this MVP text simulation, we pass the prompt directly.
        response = model.generate_content([prompt])
        result = json.loads(response.text)
        
        complaint.ai_waste_type = result.get("ai_waste_type")
        complaint.ai_severity = result.get("ai_severity")
        complaint.ai_suggested_category = result.get("ai_suggested_category")
        complaint.ai_description = result.get("ai_description")
        complaint.ai_classified_at = datetime.utcnow()
        
        db.commit()
        db.refresh(complaint)
        logger.info(f"Successfully classified complaint {complaint_id} via Gemini")
        
    except Exception as e:
        logger.error(f"Gemini classification failed for {complaint_id}: {str(e)}")
        # In a failure, we just leave the AI fields null and proceed
        
    return complaint
