import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { 
  ArrowLeft, 
  MapPin, 
  Clock, 
  User, 
  Calendar,
  MessageCircle,
  Plus,
  Send,
  Eye,
  EyeOff
} from 'lucide-react'
import { api } from '../services/api'
import { Issue, CreateCommentData, CreateProgressUpdateData } from '../types'
import { useAuth } from '../hooks/useAuth'
import { format } from 'date-fns'
import toast from 'react-hot-toast'

const IssueDetails = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [newComment, setNewComment] = useState('')
  const [newProgressDescription, setNewProgressDescription] = useState('')
  const [showInternalComments, setShowInternalComments] = useState(false)

  const { data: issue, isLoading } = useQuery(
    ['issue', id],
    async () => {
      const response = await api.get(`/issues/${id}`)
      return response.data
    }
  )

  const addCommentMutation = useMutation(
    async (data: CreateCommentData) => {
      const response = await api.post(`/issues/${id}/comments`, data)
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['issue', id])
        setNewComment('')
        toast.success('Comment added successfully')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to add comment')
      },
    }
  )

  const updateStatusMutation = useMutation(
    async (data: CreateProgressUpdateData) => {
      const response = await api.post(`/issues/${id}/progress`, data)
      return response.data
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['issue', id])
        toast.success('Status updated successfully')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to update status')
      },
    }
  )

  const handleAddComment = () => {
    if (!newComment.trim()) return

    addCommentMutation.mutate({
      text: newComment,
      isInternal: false
    })
  }

  const handleUpdateStatus = (status: string) => {
    if (!newProgressDescription.trim()) {
      toast.error('Please provide a description for the status update')
      return
    }

    updateStatusMutation.mutate({
      status: status as any,
      description: newProgressDescription
    })
    setNewProgressDescription('')
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4" />
      case 'in_progress':
        return <Clock className="w-4 h-4" />
      case 'completed':
        return <Clock className="w-4 h-4" />
      default:
        return <Clock className="w-4 h-4" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'status-pending'
      case 'in_progress':
        return 'status-in-progress'
      case 'completed':
        return 'status-completed'
      default:
        return 'status-pending'
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'pothole':
        return '🕳️'
      case 'garbage':
        return '🗑️'
      case 'streetlight':
        return '💡'
      case 'water':
        return '💧'
      case 'electricity':
        return '⚡'
      case 'road':
        return '🛣️'
      case 'sewage':
        return '🚰'
      default:
        return '📋'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'text-red-600 bg-red-100'
      case 'high':
        return 'text-orange-600 bg-orange-100'
      case 'medium':
        return 'text-yellow-600 bg-yellow-100'
      case 'low':
        return 'text-green-600 bg-green-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!issue) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Issue not found</h2>
        <button
          onClick={() => navigate(-1)}
          className="btn-primary"
        >
          Go Back
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate(-1)}
          className="btn-secondary flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Issue Details</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Issue Info */}
          <div className="card">
            <div className="flex items-start gap-4 mb-4">
              <span className="text-4xl">{getCategoryIcon(issue.category)}</span>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-2xl font-bold text-gray-900">{issue.title}</h2>
                  <span className={`${getStatusColor(issue.status)} flex items-center gap-1`}>
                    {getStatusIcon(issue.status)}
                    {issue.status.replace('_', ' ')}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(issue.priority)}`}>
                    {issue.priority}
                  </span>
                </div>
                <p className="text-gray-600 text-lg">{issue.description}</p>
              </div>
            </div>

            {/* Images */}
            {issue.images && issue.images.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Images</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {issue.images.map((image, index) => (
                    <img
                      key={index}
                      src={image}
                      alt={`Issue image ${index + 1}`}
                      className="w-full h-32 object-cover rounded-lg"
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Location */}
            <div className="flex items-center gap-2 text-gray-600">
              <MapPin className="w-5 h-5" />
              <span>{issue.location.address}</span>
            </div>
          </div>

          {/* Comments */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Comments</h3>
              {user?.role === 'admin' && (
                <button
                  onClick={() => setShowInternalComments(!showInternalComments)}
                  className="btn-secondary flex items-center gap-2"
                >
                  {showInternalComments ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  {showInternalComments ? 'Hide Internal' : 'Show Internal'}
                </button>
              )}
            </div>

            {/* Add Comment */}
            <div className="mb-6">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add a comment..."
                  className="input-field flex-1"
                />
                <button
                  onClick={handleAddComment}
                  disabled={addCommentMutation.isLoading}
                  className="btn-primary flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  Send
                </button>
              </div>
            </div>

            {/* Comments List */}
            <div className="space-y-4">
              {issue.comments
                ?.filter(comment => user?.role === 'admin' || !comment.isInternal)
                .map((comment) => (
                  <div key={comment.id} className="border-l-4 border-primary-200 pl-4">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-gray-900">{comment.authorName}</span>
                      <span className="text-sm text-gray-500">
                        {format(new Date(comment.createdAt), 'MMM dd, yyyy HH:mm')}
                      </span>
                      {comment.isInternal && (
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                          Internal
                        </span>
                      )}
                    </div>
                    <p className="text-gray-700">{comment.text}</p>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Issue Details */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Issue Details</h3>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-600">Reported by</span>
                <p className="text-gray-900">{issue.reportedBy}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-600">Created</span>
                <p className="text-gray-900">
                  {format(new Date(issue.createdAt), 'MMM dd, yyyy HH:mm')}
                </p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-600">Last Updated</span>
                <p className="text-gray-900">
                  {format(new Date(issue.updatedAt), 'MMM dd, yyyy HH:mm')}
                </p>
              </div>
              {issue.resolvedAt && (
                <div>
                  <span className="text-sm font-medium text-gray-600">Resolved</span>
                  <p className="text-gray-900">
                    {format(new Date(issue.resolvedAt), 'MMM dd, yyyy HH:mm')}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Admin Actions */}
          {user?.role === 'admin' && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Admin Actions</h3>
              
              {/* Status Update */}
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Update Status
                  </label>
                  <div className="space-y-2">
                    <button
                      onClick={() => handleUpdateStatus('in_progress')}
                      disabled={updateStatusMutation.isLoading || issue.status === 'in_progress'}
                      className="btn-warning w-full text-sm"
                    >
                      Mark as In Progress
                    </button>
                    <button
                      onClick={() => handleUpdateStatus('completed')}
                      disabled={updateStatusMutation.isLoading || issue.status === 'completed'}
                      className="btn-success w-full text-sm"
                    >
                      Mark as Completed
                    </button>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Status Description
                  </label>
                  <textarea
                    value={newProgressDescription}
                    onChange={(e) => setNewProgressDescription(e.target.value)}
                    placeholder="Describe the progress or resolution..."
                    className="input-field"
                    rows={3}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Progress Updates */}
          {issue.progress && issue.progress.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Updates</h3>
              <div className="space-y-3">
                {issue.progress.map((update) => (
                  <div key={update.id} className="border-l-4 border-primary-200 pl-4">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(update.status)}`}>
                        {update.status.replace('_', ' ')}
                      </span>
                      <span className="text-sm text-gray-500">
                        {format(new Date(update.createdAt), 'MMM dd, HH:mm')}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700">{update.description}</p>
                    <p className="text-xs text-gray-500">by {update.updatedByName}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default IssueDetails
