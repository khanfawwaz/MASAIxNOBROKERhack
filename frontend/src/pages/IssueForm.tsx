import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'react-query'
import { 
  MapPin, 
  Upload, 
  X, 
  Camera,
  AlertCircle,
  CheckCircle
} from 'lucide-react'
import { api } from '../services/api'
import { CreateIssueData, IssueCategory, IssuePriority } from '../types'
import toast from 'react-hot-toast'

const IssueForm = () => {
  const navigate = useNavigate()
  const [images, setImages] = useState<File[]>([])
  const [location, setLocation] = useState<{ lat: number; lng: number; address: string } | null>(null)
  const [isGettingLocation, setIsGettingLocation] = useState(false)

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<CreateIssueData>()

  const createIssueMutation = useMutation(
    async (data: CreateIssueData) => {
      const formData = new FormData()
      formData.append('title', data.title)
      formData.append('description', data.description)
      formData.append('category', data.category)
      formData.append('priority', data.priority)
      formData.append('location', JSON.stringify(data.location))
      
      images.forEach((image, index) => {
        formData.append(`images`, image)
      })

      const response = await api.post('/issues', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response.data
    },
    {
      onSuccess: () => {
        toast.success('Issue reported successfully!')
        navigate('/citizen')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to report issue')
      },
    }
  )

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      toast.error('Geolocation is not supported by this browser')
      return
    }

    setIsGettingLocation(true)
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords
        
        try {
          // Reverse geocoding to get address
          const response = await fetch(
            `https://api.opencagedata.com/geocode/v1/json?q=${latitude}+${longitude}&key=YOUR_OPENCAGE_API_KEY`
          )
          const data = await response.json()
          
          if (data.results && data.results.length > 0) {
            const address = data.results[0].formatted
            setLocation({ lat: latitude, lng: longitude, address })
            setValue('location', {
              address,
              coordinates: { lat: latitude, lng: longitude }
            })
            toast.success('Location detected successfully!')
          } else {
            setLocation({ lat: latitude, lng: longitude, address: 'Location detected' })
            setValue('location', {
              address: 'Location detected',
              coordinates: { lat: latitude, lng: longitude }
            })
            toast.success('Location detected! Please enter the address manually.')
          }
        } catch (error) {
          setLocation({ lat: latitude, lng: longitude, address: 'Location detected' })
          setValue('location', {
            address: 'Location detected',
            coordinates: { lat: latitude, lng: longitude }
          })
          toast.success('Location detected! Please enter the address manually.')
        }
        
        setIsGettingLocation(false)
      },
      (error) => {
        console.error('Error getting location:', error)
        toast.error('Failed to get your location. Please enter it manually.')
        setIsGettingLocation(false)
      }
    )
  }

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    const validFiles = files.filter(file => {
      if (file.size > 5 * 1024 * 1024) {
        toast.error('File size must be less than 5MB')
        return false
      }
      if (!file.type.startsWith('image/')) {
        toast.error('Only image files are allowed')
        return false
      }
      return true
    })
    
    setImages(prev => [...prev, ...validFiles].slice(0, 5)) // Max 5 images
  }

  const removeImage = (index: number) => {
    setImages(prev => prev.filter((_, i) => i !== index))
  }

  const onSubmit = (data: CreateIssueData) => {
    if (!location) {
      toast.error('Please select a location')
      return
    }

    if (images.length === 0) {
      toast.error('Please upload at least one image')
      return
    }

    createIssueMutation.mutate({
      ...data,
      images
    })
  }

  const categories: { value: IssueCategory; label: string; icon: string }[] = [
    { value: 'pothole', label: 'Pothole', icon: '🕳️' },
    { value: 'garbage', label: 'Garbage', icon: '🗑️' },
    { value: 'streetlight', label: 'Streetlight', icon: '💡' },
    { value: 'water', label: 'Water Issue', icon: '💧' },
    { value: 'electricity', label: 'Electricity', icon: '⚡' },
    { value: 'road', label: 'Road Issue', icon: '🛣️' },
    { value: 'sewage', label: 'Sewage', icon: '🚰' },
    { value: 'other', label: 'Other', icon: '📋' },
  ]

  const priorities: { value: IssuePriority; label: string; color: string }[] = [
    { value: 'low', label: 'Low', color: 'text-green-600 bg-green-100' },
    { value: 'medium', label: 'Medium', color: 'text-yellow-600 bg-yellow-100' },
    { value: 'high', label: 'High', color: 'text-orange-600 bg-orange-100' },
    { value: 'urgent', label: 'Urgent', color: 'text-red-600 bg-red-100' },
  ]

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8 text-center">
        <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center mb-4">
          <span className="text-2xl">🏛️</span>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Report a Civic Issue</h1>
        <p className="text-gray-600">Help improve your community by reporting local issues</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Basic Information</h3>
          
          {/* Title */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Issue Title *
            </label>
            <input
              {...register('title', { required: 'Title is required' })}
              type="text"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Brief description of the issue"
            />
            {errors.title && (
              <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <textarea
              {...register('description', { required: 'Description is required' })}
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Provide detailed information about the issue"
            />
            {errors.description && (
              <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
            )}
          </div>
        </div>

        {/* Category and Priority */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Category & Priority</h3>
          
          {/* Category */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Category *
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {categories.map((category) => (
                <label
                  key={category.value}
                  className="flex items-center p-4 border-2 border-gray-200 rounded-xl cursor-pointer hover:border-blue-300 hover:bg-blue-50 transition-all duration-200"
                >
                  <input
                    {...register('category', { required: 'Category is required' })}
                    type="radio"
                    value={category.value}
                    className="sr-only"
                  />
                  <div className="text-2xl mr-3">{category.icon}</div>
                  <span className="text-sm font-medium">{category.label}</span>
                </label>
              ))}
            </div>
            {errors.category && (
              <p className="text-red-500 text-sm mt-2">{errors.category.message}</p>
            )}
          </div>

          {/* Priority */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Priority Level *
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {priorities.map((priority) => (
                <label
                  key={priority.value}
                  className="flex items-center justify-center p-4 border-2 border-gray-200 rounded-xl cursor-pointer hover:border-blue-300 hover:bg-blue-50 transition-all duration-200"
                >
                  <input
                    {...register('priority', { required: 'Priority is required' })}
                    type="radio"
                    value={priority.value}
                    className="sr-only"
                  />
                  <span className={`px-3 py-2 rounded-full text-sm font-medium ${priority.color}`}>
                    {priority.label}
                  </span>
                </label>
              ))}
            </div>
            {errors.priority && (
              <p className="text-red-500 text-sm mt-2">{errors.priority.message}</p>
            )}
          </div>
        </div>

        {/* Location */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Location</h3>
          
          <div className="space-y-4">
            <button
              type="button"
              onClick={getCurrentLocation}
              disabled={isGettingLocation}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <MapPin className="w-5 h-5" />
              {isGettingLocation ? 'Getting Location...' : 'Use Current Location'}
            </button>
            
            {location && (
              <div className="p-4 bg-green-50 border-2 border-green-200 rounded-xl">
                <div className="flex items-center gap-2 text-green-800 mb-2">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">Location detected</span>
                </div>
                <p className="text-sm text-green-700">{location.address}</p>
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Address *
              </label>
              <input
                {...register('location.address', { required: 'Location is required' })}
                type="text"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Enter the exact location of the issue"
                value={location?.address || ''}
                onChange={(e) => {
                  if (location) {
                    setLocation({ ...location, address: e.target.value })
                  }
                }}
              />
              {errors.location && (
                <p className="text-red-500 text-sm mt-1">{errors.location.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Images */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Photos</h3>
          
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 hover:bg-blue-50 transition-all duration-200">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="cursor-pointer flex flex-col items-center"
              >
                <Camera className="w-12 h-12 text-gray-400 mb-4" />
                <span className="text-lg font-medium text-gray-600 mb-2">Upload Photos</span>
                <span className="text-sm text-gray-500">PNG, JPG up to 5MB each (max 5 photos)</span>
              </label>
            </div>
            
            {images.length > 0 && (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {images.map((image, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`Upload ${index + 1}`}
                      className="w-full h-32 object-cover rounded-xl"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Submit */}
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => navigate('/citizen')}
            className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={createIssueMutation.isLoading}
            className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {createIssueMutation.isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Reporting Issue...
              </>
            ) : (
              'Report Issue'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

export default IssueForm
