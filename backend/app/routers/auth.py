
# Authentication Routes
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserLogin, LoginResponse, RegisterResponse, PasswordChange
from ..services.auth import AuthService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    try:
        user = AuthService.register_user(db, user_data)
        token_data = AuthService.create_user_token(user)
        
        return RegisterResponse(
            success=True,
            message="User registered successfully",
            data={
                "access_token": token_data["access_token"],
                "token_type": token_data["token_type"],
                "expires_in": token_data["expires_in"],
                "user": token_data["user"]
            }
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    try:
        user = AuthService.authenticate_user(
            db, 
            user_credentials.email, 
            user_credentials.password
        )
        
        token_data = AuthService.create_user_token(user)
        
        return LoginResponse(
            success=True,
            message="Login successful",
            data={
                "access_token": token_data["access_token"],
                "token_type": token_data["token_type"],
                "expires_in": token_data["expires_in"],
                "user": token_data["user"]
            }
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    
    return {
        "success": True,
        "data": current_user.to_dict()
    }

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    try:
        AuthService.change_password(db, current_user, password_data)
        
        return {
            "success": True,
            "message": "Password updated successfully"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )