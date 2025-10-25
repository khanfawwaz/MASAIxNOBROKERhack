import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'
import Layout from './components/Layout'
import Login from './pages/Login'
import CitizenDashboard from './pages/CitizenDashboard'
import AdminDashboard from './pages/AdminDashboard'
import IssueForm from './pages/IssueForm'
import IssueDetails from './pages/IssueDetails'
import Profile from './pages/Profile'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to={user?.role === 'admin' ? '/admin' : '/citizen'} />} />
        <Route path="citizen" element={user?.role === 'citizen' ? <CitizenDashboard /> : <Navigate to="/login" />} />
        <Route path="admin" element={user?.role === 'admin' ? <AdminDashboard /> : <Navigate to="/login" />} />
        <Route path="issue/new" element={user?.role === 'citizen' ? <IssueForm /> : <Navigate to="/login" />} />
        <Route path="issue/:id" element={<IssueDetails />} />
        <Route path="profile" element={<Profile />} />
      </Route>
    </Routes>
  )
}

export default App
