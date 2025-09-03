# File Processing Service
import io
import re
from typing import Dict, Any, Optional
import textstat
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from fastapi import HTTPException
import PyPDF2
import docx

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class FileService:
    
    @staticmethod
    def extract_text_from_file(file_content: bytes, filename: str, content_type: str) -> str:
        """Extract text from uploaded file based on type"""
        
        try:
            if content_type == "text/plain" or filename.endswith('.txt'):
                return file_content.decode('utf-8')
            
            elif content_type == "application/pdf" or filename.endswith('.pdf'):
                return FileService._extract_pdf_text(file_content)
            
            elif (content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
                  or filename.endswith('.docx')):
                return FileService._extract_docx_text(file_content)
            
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {content_type}"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text from file: {str(e)}"
            )
    
    @staticmethod
    def _extract_pdf_text(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="No text found in PDF file"
                )
            
            return text
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process PDF file: {str(e)}"
            )
    
    @staticmethod
    def _extract_docx_text(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="No text found in DOCX file"
                )
            
            return text
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process DOCX file: {str(e)}"
            )

class AnalysisService:
    
    @staticmethod
    def get_database_metrics(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metrics for database storage"""
        return {
            "flesch_kincaid_grade_level": analysis_result["flesch_kincaid_grade"],
            "gunning_fog_index": analysis_result["gunning_fog_index"],
            "smog_index": analysis_result["smog_index"]
        }
    
    @staticmethod
    def analyze_text_readability(text: str) -> Dict[str, Any]:
        """Perform comprehensive readability analysis"""
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 10 characters long"
            )
        
        try:
            # Clean text
            text = text.strip()
            
            # Basic text statistics
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            word_count = len([w for w in words if w.isalpha()])
            sentence_count = len(sentences)
            
            if sentence_count == 0 or word_count == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Text must contain at least one sentence and word"
                )
            
            # Character count (excluding spaces)
            char_count = len(re.sub(r'\s', '', text))
            
            # Average metrics
            avg_sentence_length = word_count / sentence_count
            
            # Readability scores using textstat
            flesch_ease = textstat.flesch_reading_ease(text)
            flesch_grade = textstat.flesch_kincaid_grade(text)
            gunning_fog = textstat.gunning_fog(text)
            smog_index = textstat.smog_index(text)
            
            # Determine complexity level and color
            complexity_level, complexity_color = AnalysisService._determine_complexity(flesch_ease)
            
            # Reading time estimate (average 200 WPM)
            reading_time_minutes = max(0.5, round(word_count / 200, 1))
            
            return {
                # Basic statistics
                "word_count": word_count,
                "sentence_count": sentence_count,
                "character_count": char_count,
                "avg_sentence_length": round(avg_sentence_length, 2),
                
                # Readability scores
                "flesch_reading_ease": round(flesch_ease, 1),
                "flesch_kincaid_grade": round(flesch_grade, 1),
                "gunning_fog_index": round(gunning_fog, 1),
                "smog_index": round(smog_index, 1),
                
                # Interpretations
                "complexity_level": complexity_level,
                "complexity_color": complexity_color,
                "flesch_interpretation": AnalysisService._interpret_flesch_ease(flesch_ease),
                "grade_level_interpretation": AnalysisService._interpret_grade_level(flesch_grade),
                
                # Additional metrics
                "reading_time_minutes": reading_time_minutes,
                "text_preview": text[:200] + "..." if len(text) > 200 else text
            }
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )
    
    @staticmethod
    def _determine_complexity(flesch_ease: float) -> tuple[str, str]:
        """Determine complexity level and color"""
        if flesch_ease >= 70:
            return "Beginner", "#28a745"  # Green
        elif flesch_ease >= 30:
            return "Intermediate", "#ffc107"  # Yellow
        else:
            return "Advanced", "#dc3545"  # Red
    
    @staticmethod
    def _interpret_flesch_ease(score: float) -> str:
        """Interpret Flesch Reading Ease score"""
        if score >= 90:
            return "Very Easy (5th grade)"
        elif score >= 80:
            return "Easy (6th grade)"
        elif score >= 70:
            return "Fairly Easy (7th grade)"
        elif score >= 60:
            return "Standard (8th-9th grade)"
        elif score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (Graduate)"
    
    @staticmethod
    def _interpret_grade_level(grade: float) -> str:
        """Interpret grade level score"""
        if grade <= 6:
            return "Elementary School"
        elif grade <= 8:
            return "Middle School"
        elif grade <= 12:
            return "High School"
        elif grade <= 16:
            return "College"
        else:
            return "Graduate Level"