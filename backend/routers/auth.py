from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from bson import ObjectId
from datetime import datetime, timedelta
from typing import List

from models import User, UserCreate, UserLogin, UserResponse, Token
from auth import verify_password, get_password_hash, create_access_token, get_current_user
from database import get_database
from email_service import email_service

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user_dict = {
        "email": user_data.email,
        "name": user_data.name,
        "role": user_data.role,
        "phone": user_data.phone,
        "address": user_data.address,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user_dict["_id"])}, expires_delta=access_token_expires
    )
    
    # Return user data without password
    user_response = UserResponse(
        id=str(user_dict["_id"]),
        email=user_dict["email"],
        name=user_dict["name"],
        role=user_dict["role"],
        phone=user_dict.get("phone"),
        address=user_dict.get("address"),
        created_at=user_dict["created_at"],
        updated_at=user_dict["updated_at"]
    )
    
    # Send welcome email asynchronously
    try:
        await email_service.send_welcome_email(
            user_dict["email"], 
            user_dict["name"], 
            user_dict["role"]
        )
    except Exception as e:
        # Log error but don't fail registration
        print(f"Failed to send welcome email: {e}")
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    db = await get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    # Return user data without password
    user_response = UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        role=user["role"],
        phone=user.get("phone"),
        address=user.get("address"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )
    
    # Send login notification email asynchronously
    try:
        login_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        await email_service.send_login_notification(
            user["email"], 
            user["name"], 
            login_time
        )
    except Exception as e:
        # Log error but don't fail login
        print(f"Failed to send login notification: {e}")
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user_id: str = Depends(get_current_user)):
    db = await get_database()
    
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        role=user["role"],
        phone=user.get("phone"),
        address=user.get("address"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: dict,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    # Update user profile
    update_data = {
        "name": profile_data.get("name"),
        "phone": profile_data.get("phone"),
        "address": profile_data.get("address"),
        "updated_at": datetime.utcnow()
    }
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    result = await db.users.update_one(
        {"_id": ObjectId(current_user_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return updated user
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        role=user["role"],
        phone=user.get("phone"),
        address=user.get("address"),
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )

@router.get("/stats")
async def get_user_stats(current_user_id: str = Depends(get_current_user)):
    db = await get_database()
    
    # Get user info
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user["role"] == "citizen":
        # Citizen stats
        total_issues = await db.issues.count_documents({"reported_by": current_user_id})
        pending_issues = await db.issues.count_documents({
            "reported_by": current_user_id,
            "status": "pending"
        })
        in_progress_issues = await db.issues.count_documents({
            "reported_by": current_user_id,
            "status": "in_progress"
        })
        completed_issues = await db.issues.count_documents({
            "reported_by": current_user_id,
            "status": "completed"
        })
        
        return {
            "totalIssues": total_issues,
            "pendingIssues": pending_issues,
            "inProgressIssues": in_progress_issues,
            "completedIssues": completed_issues
        }
    
    else:
        # Admin stats
        total_issues = await db.issues.count_documents({})
        resolved_issues = await db.issues.count_documents({"status": "completed"})
        
        # Calculate response rate (issues with at least one comment or progress update)
        responded_issues = await db.issues.count_documents({
            "$or": [
                {"comments": {"$exists": True, "$ne": []}},
                {"progress": {"$exists": True, "$ne": []}}
            ]
        })
        
        response_rate = (responded_issues / total_issues * 100) if total_issues > 0 else 0
        
        return {
            "totalIssues": total_issues,
            "resolvedIssues": resolved_issues,
            "responseRate": round(response_rate, 2)
        }
