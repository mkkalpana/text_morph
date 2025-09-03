# Analysis Routes - Updated for simplified database storage
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import TextAnalysisRequest, TextAnalysisResponse, FileAnalysisResponse
from ..services.file import FileService, AnalysisService
from ..utils.security import get_current_user
from ..models.user import User
from ..models.analysis_history import AnalysisHistory
from ..config import settings

router = APIRouter(prefix="/analysis", tags=["Text Analysis"])

@router.post("/file", response_model=FileAnalysisResponse)
async def analyze_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze uploaded file for readability"""
    
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        # Extract text from file
        text = FileService.extract_text_from_file(
            file_content, 
            file.filename, 
            file.content_type
        )
        
        # Analyze text - gets all metrics for display
        analysis_result = AnalysisService.analyze_text_readability(text)
        
        # Save only the 3 metrics we want to database
        db_metrics = AnalysisService.get_database_metrics(analysis_result)
        
        db_history = AnalysisHistory(
            user_id=current_user.id,
            file_name=file.filename,
            analysis_type="file",
            flesch_kincaid_grade_level=db_metrics["flesch_kincaid_grade_level"],
            gunning_fog_index=db_metrics["gunning_fog_index"],
            smog_index=db_metrics["smog_index"]
        )
        
        db.add(db_history)
        db.commit()
        
        return FileAnalysisResponse(
            success=True,
            filename=file.filename,
            file_size=len(file_content),
            analysis=analysis_result,  # Return all metrics for display
            message="File analyzed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File analysis failed: {str(e)}"
        )

@router.post("/text", response_model=TextAnalysisResponse)
async def analyze_text(
    text_data: TextAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze text for readability"""
    
    try:
        # Analyze text - gets all metrics for display
        analysis_result = AnalysisService.analyze_text_readability(text_data.text)
        
        # Save only the 3 metrics we want to database
        db_metrics = AnalysisService.get_database_metrics(analysis_result)
        
        db_history = AnalysisHistory(
            user_id=current_user.id,
            file_name=None,  # No file for text input
            analysis_type="text",
            flesch_kincaid_grade_level=db_metrics["flesch_kincaid_grade_level"],
            gunning_fog_index=db_metrics["gunning_fog_index"],
            smog_index=db_metrics["smog_index"]
        )
        
        db.add(db_history)
        db.commit()
        
        return TextAnalysisResponse(
            success=True,
            analysis=analysis_result,  # Return all metrics for display
            message="Text analyzed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text analysis failed: {str(e)}"
        )

@router.get("/history")
async def get_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's analysis history from database"""
    
    try:
        history = db.query(AnalysisHistory).filter(
            AnalysisHistory.user_id == current_user.id
        ).order_by(AnalysisHistory.created_at.desc()).limit(20).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": h.id,
                    "file_name": h.file_name,
                    "analysis_type": h.analysis_type,
                    "flesch_kincaid_grade_level": h.flesch_kincaid_grade_level,
                    "gunning_fog_index": h.gunning_fog_index,
                    "smog_index": h.smog_index,
                    "created_at": h.created_at.isoformat()
                } for h in history
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}"
        )
