import { useState, useEffect } from 'react'
import { useQuery } from 'react-query'
import { useNavigate } from 'react-router-dom'
import { 
  Plus, 
  MapPin, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Search,
  Filter,
  Eye
} from 'lucide-react'
import { api } from '../services/api'
import { Issue, IssueStatus } from '../types'
import { format } from 'date-fns'

const CitizenDashboard = () => {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<IssueStatus | 'all'>('all')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')

  const { data: issues, isLoading, refetch } = useQuery(
    ['issues', searchTerm, statusFilter, categoryFilter],
    async () => {
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (statusFilter !== 'all') params.append('status', statusFilter)
      if (categoryFilter !== 'all') params.append('category', categoryFilter)
      
      const response = await api.get(`/issues?${params.toString()}`)
      return response.data
    }
  )

  const getStatusIcon = (status: IssueStatus) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4" />
      case 'in_progress':
        return <AlertCircle className="w-4 h-4" />
      case 'completed':
        return <CheckCircle className="w-4 h-4" />
      default:
        return <Clock className="w-4 h-4" />
    }
  }

  const getStatusColor = (status: IssueStatus) => {
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

  const stats = {
    total: issues?.length || 0,
    pending: issues?.filter((issue: Issue) => issue.status === 'pending').length || 0,
    inProgress: issues?.filter((issue: Issue) => issue.status === 'in_progress').length || 0,
    completed: issues?.filter((issue: Issue) => issue.status === 'completed').length || 0,
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Issues</h1>
          <p className="text-gray-600 mt-1">Track and manage your reported civic issues</p>
        </div>
        <button
          onClick={() => navigate('/issue/new')}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center mt-4 sm:mt-0"
        >
          <Plus className="w-5 h-5 mr-2" />
          Report New Issue
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-xl">
              <AlertCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Issues</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-xl">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-gray-900">{stats.pending}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-xl">
              <AlertCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">{stats.inProgress}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-to-r from-green-100 to-emerald-100 rounded-xl">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{stats.completed}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search issues..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
          </div>
          <div className="flex gap-4">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as IssueStatus | 'all')}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
              <option value="all">All Categories</option>
              <option value="pothole">Pothole</option>
              <option value="garbage">Garbage</option>
              <option value="streetlight">Streetlight</option>
              <option value="water">Water</option>
              <option value="electricity">Electricity</option>
              <option value="road">Road</option>
              <option value="sewage">Sewage</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
      </div>

      {/* Issues List */}
      <div className="space-y-4">
        {issues?.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg border border-gray-100 text-center py-16">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-gray-100 to-gray-200 rounded-full flex items-center justify-center mb-6">
              <AlertCircle className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">No issues found</h3>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              {searchTerm || statusFilter !== 'all' || categoryFilter !== 'all'
                ? 'Try adjusting your filters to see more results.'
                : "You haven't reported any civic issues yet. Help improve your community by reporting problems you encounter."
              }
            </p>
            {!searchTerm && statusFilter === 'all' && categoryFilter === 'all' && (
              <button
                onClick={() => navigate('/issue/new')}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-8 rounded-lg transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Report Your First Issue
              </button>
            )}
          </div>
        ) : (
          issues?.map((issue: Issue) => (
            <div key={issue.id} className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 hover:scale-[1.01]">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="text-3xl">{getCategoryIcon(issue.category)}</div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{issue.title}</h3>
                      <div className="flex items-center gap-2">
                        <span className={`${getStatusColor(issue.status)} flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium`}>
                          {getStatusIcon(issue.status)}
                          {issue.status.replace('_', ' ')}
                        </span>
                        <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                          {issue.priority}
                        </span>
                      </div>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-4 line-clamp-2">{issue.description}</p>
                  <div className="flex items-center gap-6 text-sm text-gray-500">
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-blue-500" />
                      <span className="truncate max-w-xs">{issue.location.address}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-gray-400" />
                      {format(new Date(issue.createdAt), 'MMM dd, yyyy')}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => navigate(`/issue/${issue.id}`)}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 transform hover:scale-[1.05] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center gap-2 ml-4"
                >
                  <Eye className="w-4 h-4" />
                  View Details
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default CitizenDashboard
