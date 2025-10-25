import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation, useQuery } from 'react-query'
import { User, Mail, Phone, MapPin, Save, Edit3 } from 'lucide-react'
import { api } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import toast from 'react-hot-toast'

interface ProfileData {
  name: string
  email: string
  phone?: string
  address?: string
}

const Profile = () => {
  const { user, login } = useAuth()
  const [isEditing, setIsEditing] = useState(false)

  const { register, handleSubmit, formState: { errors }, reset } = useForm<ProfileData>({
    defaultValues: {
      name: user?.name || '',
      email: user?.email || '',
      phone: user?.phone || '',
      address: user?.address || '',
    }
  })

  const { data: userStats } = useQuery(
    'user-stats',
    async () => {
      const response = await api.get('/auth/stats')
      return response.data
    }
  )

  const updateProfileMutation = useMutation(
    async (data: ProfileData) => {
      const response = await api.put('/auth/profile', data)
      return response.data
    },
    {
      onSuccess: (data) => {
        // Update the user context
        login(user?.email || '', '') // This will trigger a re-fetch
        setIsEditing(false)
        toast.success('Profile updated successfully')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to update profile')
      },
    }
  )

  const onSubmit = (data: ProfileData) => {
    updateProfileMutation.mutate(data)
  }

  const handleCancel = () => {
    reset()
    setIsEditing(false)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Profile</h1>
        <p className="text-gray-600">Manage your account information</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Form */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Personal Information</h2>
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="btn-secondary flex items-center gap-2"
              >
                <Edit3 className="w-4 h-4" />
                {isEditing ? 'Cancel' : 'Edit'}
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    {...register('name', { required: 'Name is required' })}
                    type="text"
                    disabled={!isEditing}
                    className={`input-field pl-10 ${!isEditing ? 'bg-gray-50' : ''}`}
                  />
                </div>
                {errors.name && (
                  <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    {...register('email', { required: 'Email is required' })}
                    type="email"
                    disabled={!isEditing}
                    className={`input-field pl-10 ${!isEditing ? 'bg-gray-50' : ''}`}
                  />
                </div>
                {errors.email && (
                  <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    {...register('phone')}
                    type="tel"
                    disabled={!isEditing}
                    className={`input-field pl-10 ${!isEditing ? 'bg-gray-50' : ''}`}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Address
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    {...register('address')}
                    type="text"
                    disabled={!isEditing}
                    className={`input-field pl-10 ${!isEditing ? 'bg-gray-50' : ''}`}
                  />
                </div>
              </div>

              {isEditing && (
                <div className="flex gap-4">
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="btn-secondary flex-1"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updateProfileMutation.isLoading}
                    className="btn-primary flex-1 flex items-center justify-center gap-2"
                  >
                    {updateProfileMutation.isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4" />
                        Save Changes
                      </>
                    )}
                  </button>
                </div>
              )}
            </form>
          </div>
        </div>

        {/* Stats */}
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-600">Role</span>
                <p className="text-gray-900 capitalize">{user?.role}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-600">Member Since</span>
                <p className="text-gray-900">
                  {user?.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {user?.role === 'citizen' && userStats && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Activity</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Total Issues</span>
                  <span className="text-gray-900 font-semibold">{userStats.totalIssues || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Pending</span>
                  <span className="text-gray-900 font-semibold">{userStats.pendingIssues || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">In Progress</span>
                  <span className="text-gray-900 font-semibold">{userStats.inProgressIssues || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Completed</span>
                  <span className="text-gray-900 font-semibold">{userStats.completedIssues || 0}</span>
                </div>
              </div>
            </div>
          )}

          {user?.role === 'admin' && userStats && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Admin Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Total Issues</span>
                  <span className="text-gray-900 font-semibold">{userStats.totalIssues || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Resolved</span>
                  <span className="text-gray-900 font-semibold">{userStats.resolvedIssues || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium text-gray-600">Response Rate</span>
                  <span className="text-gray-900 font-semibold">
                    {userStats.responseRate ? `${userStats.responseRate}%` : 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile
