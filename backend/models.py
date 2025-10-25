from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime
from bson import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    name: str
    role: Literal["citizen", "admin"]
    phone: Optional[str] = None
    address: Optional[str] = None
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Literal["citizen", "admin"]
    phone: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class IssueCategory(str, Enum):
    POTHOLE = "pothole"
    GARBAGE = "garbage"
    STREETLIGHT = "streetlight"
    WATER = "water"
    ELECTRICITY = "electricity"
    ROAD = "road"
    SEWAGE = "sewage"
    OTHER = "other"

class IssuePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class IssueStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class Location(BaseModel):
    address: str
    coordinates: dict  # {"lat": float, "lng": float}

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    text: str
    author: str  # user_id
    author_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_internal: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProgressUpdate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: IssueStatus
    description: str
    updated_by: str  # user_id
    updated_by_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Issue(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    category: IssueCategory
    priority: IssuePriority
    status: IssueStatus = IssueStatus.PENDING
    location: Location
    images: List[str] = []  # URLs to uploaded images
    reported_by: str  # user_id
    assigned_to: Optional[str] = None  # user_id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    comments: List[Comment] = []
    progress: List[ProgressUpdate] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class IssueCreate(BaseModel):
    title: str
    description: str
    category: IssueCategory
    priority: IssuePriority
    location: Location

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[IssueCategory] = None
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None
    assigned_to: Optional[str] = None

class CommentCreate(BaseModel):
    text: str
    is_internal: bool = False

class ProgressUpdateCreate(BaseModel):
    status: IssueStatus
    description: str

class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    priority: str
    status: str
    location: Location
    images: List[str]
    reported_by: str
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    comments: List[Comment]
    progress: List[ProgressUpdate]

class StatsResponse(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int
    rejected: int
    category_stats: dict
    priority_stats: dict
    response_rate: Optional[float] = None
