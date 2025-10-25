from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from datetime import datetime, timedelta
from typing import List, Optional

from models import IssueResponse, StatsResponse
from auth import get_current_admin_user
from database import get_database

router = APIRouter()

@router.get("/issues", response_model=List[IssueResponse])
async def get_all_issues(
    search: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    time: Optional[str] = None,
    current_user_id: str = Depends(get_current_admin_user)
):
    db = await get_database()
    
    # Build query
    query = {}
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    if status:
        query["status"] = status
    
    if category:
        query["category"] = category
    
    # Time filter
    if time:
        now = datetime.utcnow()
        if time == "today":
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query["created_at"] = {"$gte": start_of_day}
        elif time == "week":
            week_ago = now - timedelta(days=7)
            query["created_at"] = {"$gte": week_ago}
        elif time == "month":
            month_ago = now - timedelta(days=30)
            query["created_at"] = {"$gte": month_ago}
    
    # Get issues
    issues = []
    async for issue in db.issues.find(query).sort("created_at", -1):
        issues.append(IssueResponse(**issue))
    
    return issues

@router.get("/stats", response_model=StatsResponse)
async def get_admin_stats(current_user_id: str = Depends(get_current_admin_user)):
    db = await get_database()
    
    # Basic counts
    total = await db.issues.count_documents({})
    pending = await db.issues.count_documents({"status": "pending"})
    in_progress = await db.issues.count_documents({"status": "in_progress"})
    completed = await db.issues.count_documents({"status": "completed"})
    rejected = await db.issues.count_documents({"status": "rejected"})
    
    # Category stats
    category_pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    category_stats = {}
    async for doc in db.issues.aggregate(category_pipeline):
        category_stats[doc["_id"]] = doc["count"]
    
    # Priority stats
    priority_pipeline = [
        {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    priority_stats = {}
    async for doc in db.issues.aggregate(priority_pipeline):
        priority_stats[doc["_id"]] = doc["count"]
    
    # Response rate calculation
    responded_issues = await db.issues.count_documents({
        "$or": [
            {"comments": {"$exists": True, "$ne": []}},
            {"progress": {"$exists": True, "$ne": []}}
        ]
    })
    response_rate = (responded_issues / total * 100) if total > 0 else 0
    
    return StatsResponse(
        total=total,
        pending=pending,
        in_progress=in_progress,
        completed=completed,
        rejected=rejected,
        category_stats=category_stats,
        priority_stats=priority_stats,
        response_rate=round(response_rate, 2)
    )

@router.get("/issues/{issue_id}", response_model=IssueResponse)
async def get_issue_details(
    issue_id: str,
    current_user_id: str = Depends(get_current_admin_user)
):
    db = await get_database()
    
    issue = await db.issues.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    return IssueResponse(**issue)

@router.put("/issues/{issue_id}/assign")
async def assign_issue(
    issue_id: str,
    assignee_id: str,
    current_user_id: str = Depends(get_current_admin_user)
):
    db = await get_database()
    
    # Check if assignee exists
    assignee = await db.users.find_one({"_id": ObjectId(assignee_id)})
    if not assignee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found"
        )
    
    # Update issue
    result = await db.issues.update_one(
        {"_id": ObjectId(issue_id)},
        {
            "$set": {
                "assigned_to": assignee_id,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    return {"message": "Issue assigned successfully"}

@router.get("/users")
async def get_all_users(current_user_id: str = Depends(get_current_admin_user)):
    db = await get_database()
    
    users = []
    async for user in db.users.find({}, {"hashed_password": 0}):
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        })
    
    return users
