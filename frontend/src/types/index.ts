export interface User {
  id: string
  email: string
  name: string
  role: 'citizen' | 'admin'
  phone?: string
  address?: string
  createdAt: string
  updatedAt: string
}

export interface Issue {
  id: string
  title: string
  description: string
  category: IssueCategory
  priority: IssuePriority
  status: IssueStatus
  location: {
    address: string
    coordinates: {
      lat: number
      lng: number
    }
  }
  images: string[]
  reportedBy: string
  assignedTo?: string
  createdAt: string
  updatedAt: string
  resolvedAt?: string
  comments: Comment[]
  progress: ProgressUpdate[]
}

export type IssueCategory = 
  | 'pothole'
  | 'garbage'
  | 'streetlight'
  | 'water'
  | 'electricity'
  | 'road'
  | 'sewage'
  | 'other'

export type IssuePriority = 'low' | 'medium' | 'high' | 'urgent'

export type IssueStatus = 'pending' | 'in_progress' | 'completed' | 'rejected'

export interface Comment {
  id: string
  text: string
  author: string
  authorName: string
  createdAt: string
  isInternal: boolean
}

export interface ProgressUpdate {
  id: string
  status: IssueStatus
  description: string
  updatedBy: string
  updatedByName: string
  createdAt: string
}

export interface CreateIssueData {
  title: string
  description: string
  category: IssueCategory
  priority: IssuePriority
  location: {
    address: string
    coordinates: {
      lat: number
      lng: number
    }
  }
  images: File[]
}

export interface UpdateIssueData {
  title?: string
  description?: string
  category?: IssueCategory
  priority?: IssuePriority
  status?: IssueStatus
  assignedTo?: string
}

export interface CreateCommentData {
  text: string
  isInternal?: boolean
}

export interface CreateProgressUpdateData {
  status: IssueStatus
  description: string
}

export interface LoginData {
  email: string
  password: string
}

export interface RegisterData {
  name: string
  email: string
  password: string
  phone?: string
  address?: string
  role: 'citizen' | 'admin'
}

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}
