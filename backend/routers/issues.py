from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from bson import ObjectId
from datetime import datetime
from typing import List, Optional
import os
import shutil
from pathlib import Path

from models import Issue, IssueCreate, IssueUpdate, IssueResponse, CommentCreate, ProgressUpdateCreate, Comment, ProgressUpdate
from auth import get_current_user
from database import get_database

router = APIRouter()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/", response_model=IssueResponse)
async def create_issue(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...),
    location: str = Form(...),  # JSON string
    images: List[UploadFile] = File(...),
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    # Parse location JSON
    import json
    location_data = json.loads(location)
    
    # Save uploaded images
    image_urls = []
    for image in images:
        if image.filename:
            # Create unique filename
            file_extension = Path(image.filename).suffix
            unique_filename = f"{ObjectId()}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # Store relative URL
            image_urls.append(f"/uploads/{unique_filename}")
    
    # Create issue
    issue_dict = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "pending",
        "location": location_data,
        "images": image_urls,
        "reported_by": current_user_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "comments": [],
        "progress": []
    }
    
    result = await db.issues.insert_one(issue_dict)
    issue_dict["_id"] = result.inserted_id
    
    return IssueResponse(**issue_dict)

@router.get("/", response_model=List[IssueResponse])
async def get_issues(
    search: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    # Build query
    query = {}
    
    # Filter by user role
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if user["role"] == "citizen":
        query["reported_by"] = current_user_id
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    if status:
        query["status"] = status
    
    if category:
        query["category"] = category
    
    # Get issues
    issues = []
    async for issue in db.issues.find(query).sort("created_at", -1):
        issues.append(IssueResponse(**issue))
    
    return issues

@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    issue = await db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check permissions
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if user["role"] == "citizen" and issue["reported_by"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return IssueResponse(**issue)

@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: str,
    issue_update: IssueUpdate,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    issue = await db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check permissions
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if user["role"] == "citizen" and issue["reported_by"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update issue
    update_data = issue_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Return updated issue
    updated_issue = await db.issues.find_one({"_id": ObjectId(issue_id)})
    return IssueResponse(**updated_issue)

@router.post("/{issue_id}/comments", response_model=Comment)
async def add_comment(
    issue_id: str,
    comment_data: CommentCreate,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    # Get user info
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create comment
    comment_dict = {
        "text": comment_data.text,
        "author": current_user_id,
        "author_name": user["name"],
        "created_at": datetime.utcnow(),
        "is_internal": comment_data.is_internal
    }
    
    # Add comment to issue
    result = await db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {
            "$push": {"comments": comment_dict},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    return Comment(**comment_dict)

@router.post("/{issue_id}/progress", response_model=ProgressUpdate)
async def add_progress_update(
    issue_id: str,
    progress_data: ProgressUpdateCreate,
    current_user_id: str = Depends(get_current_user)
):
    db = await get_database()
    
    # Get user info
    user = await db.users.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create progress update
    progress_dict = {
        "status": progress_data.status,
        "description": progress_data.description,
        "updated_by": current_user_id,
        "updated_by_name": user["name"],
        "created_at": datetime.utcnow()
    }
    
    # Update issue status and add progress update
    update_data = {
        "$push": {"progress": progress_dict},
        "$set": {
            "status": progress_data.status,
            "updated_at": datetime.utcnow()
        }
    }
    
    # Set resolved_at if status is completed
    if progress_data.status == "completed":
        update_data["$set"]["resolved_at"] = datetime.utcnow()
    
    result = await db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        update_data
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    return ProgressUpdate(**progress_dict)
