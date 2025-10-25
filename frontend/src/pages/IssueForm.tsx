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
  const [selectedCategory, setSelectedCategory] = useState<IssueCategory | null>(null)
  const [selectedPriority, setSelectedPriority] = useState<IssuePriority | null>(null)

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
          // For demo purposes, we'll use a simple address format
          // In production, you would use a geocoding service like OpenCage, Google Maps, etc.
          const address = `Location: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`
          setLocation({ lat: latitude, lng: longitude, address })
          setValue('location', {
            address,
            coordinates: { lat: latitude, lng: longitude }
          })
          toast.success('Location detected! Please verify and update the address if needed.')
        } catch (error) {
          console.error('Error getting location:', error)
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

    if (!selectedCategory) {
      toast.error('Please select a category')
      return
    }

    if (!selectedPriority) {
      toast.error('Please select a priority')
      return
    }

    if (images.length === 0) {
      toast.error('Please upload at least one image')
      return
    }

    createIssueMutation.mutate({
      ...data,
      category: selectedCategory,
      priority: selectedPriority,
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
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Report an Issue</h1>
        <p className="text-gray-600">Help us make your community better by reporting issues</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Issue Title *
          </label>
          <input
            {...register('title', { required: 'Title is required' })}
            type="text"
            className="input-field"
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
            className="input-field"
            placeholder="Provide detailed information about the issue"
          />
          {errors.description && (
            <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
          )}
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category *
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {categories.map((category) => (
              <button
                key={category.value}
                type="button"
                onClick={() => {
                  setSelectedCategory(category.value)
                  setValue('category', category.value)
                }}
                className={`flex items-center p-3 border rounded-lg cursor-pointer transition-all duration-200 transform hover:scale-105 ${
                  selectedCategory === category.value
                    ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-200 shadow-md'
                    : 'border-gray-300 hover:bg-gray-50 hover:border-gray-400 hover:shadow-sm'
                }`}
              >
                <div className="text-2xl mr-2">{category.icon}</div>
                <span className="text-sm font-medium">{category.label}</span>
              </button>
            ))}
          </div>
          {errors.category && (
            <p className="text-red-500 text-sm mt-1">{errors.category.message}</p>
          )}
          {!selectedCategory && (
            <p className="text-gray-500 text-sm mt-1">Please select a category for your issue</p>
          )}
        </div>

        {/* Priority */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Priority *
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {priorities.map((priority) => (
              <button
                key={priority.value}
                type="button"
                onClick={() => {
                  setSelectedPriority(priority.value)
                  setValue('priority', priority.value)
                }}
                className={`flex items-center justify-center p-3 border rounded-lg cursor-pointer transition-all duration-200 transform hover:scale-105 ${
                  selectedPriority === priority.value
                    ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-200 shadow-md'
                    : 'border-gray-300 hover:bg-gray-50 hover:border-gray-400 hover:shadow-sm'
                }`}
              >
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${priority.color}`}>
                  {priority.label}
                </span>
              </button>
            ))}
          </div>
          {errors.priority && (
            <p className="text-red-500 text-sm mt-1">{errors.priority.message}</p>
          )}
          {!selectedPriority && (
            <p className="text-gray-500 text-sm mt-1">Please select a priority level for your issue</p>
          )}
        </div>

        {/* Location */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Location *
          </label>
          <div className="space-y-3">
            <button
              type="button"
              onClick={getCurrentLocation}
              disabled={isGettingLocation}
              className="btn-secondary flex items-center gap-2"
            >
              <MapPin className="w-5 h-5" />
              {isGettingLocation ? 'Getting Location...' : 'Use Current Location'}
            </button>
            
            {location && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center gap-2 text-green-800">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">Location detected</span>
                </div>
                <p className="text-sm text-green-700 mt-1">{location.address}</p>
              </div>
            )}
            
            <input
              {...register('location.address', { required: 'Location is required' })}
              type="text"
              className="input-field"
              placeholder="Enter the exact location of the issue"
              value={location?.address || ''}
              onChange={(e) => {
                if (location) {
                  setLocation({ ...location, address: e.target.value })
                }
              }}
            />
          </div>
          {errors.location && (
            <p className="text-red-500 text-sm mt-1">{errors.location.message}</p>
          )}
        </div>

        {/* Images */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Images * (Max 5 images)
          </label>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
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
                <Camera className="w-8 h-8 text-gray-400 mb-2" />
                <span className="text-sm text-gray-600">Click to upload images</span>
                <span className="text-xs text-gray-500 mt-1">PNG, JPG up to 5MB each</span>
              </label>
            </div>
            
            {images.length > 0 && (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {images.map((image, index) => (
                  <div key={index} className="relative">
                    <img
                      src={URL.createObjectURL(image)}
                      alt={`Upload ${index + 1}`}
                      className="w-full h-24 object-cover rounded-lg"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
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
            className="btn-secondary flex-1"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={createIssueMutation.isLoading}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {createIssueMutation.isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Reporting...
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
