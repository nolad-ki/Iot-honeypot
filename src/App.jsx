import React, { Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './components/AuthContext'
import DebugDashboard from './components/DebugDashboard'
import './App.css'

// Lazy load components for better performance
const Login = React.lazy(() => import('./components/Login'))
const Register = React.lazy(() => import('./components/Register'))
const Dashboard = React.lazy(() => import('./components/Dashboard'))
const HoneypotSettings = React.lazy(() => import('./components/HoneypotSettings'))
const LogAnalysis = React.lazy(() => import('./components/LogAnalysis'))
const Analytics = React.lazy(() => import('./components/Analytics'))

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth()
  console.log('ProtectedRoute - user:', user)
  return user ? children : <Navigate to="/login" />
}

// Error Boundary Component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('App Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          padding: '20px', 
          fontFamily: 'Arial', 
          background: '#fff3cd', 
          color: '#856404',
          minHeight: '100vh'
        }}>
          <h1>🚨 Something went wrong</h1>
          <p><strong>Error:</strong> {this.state.error?.toString()}</p>
          <div style={{ marginTop: '20px' }}>
            <button 
              onClick={() => window.location.reload()}
              style={{ 
                padding: '10px 20px', 
                background: '#856404', 
                color: 'white', 
                border: 'none', 
                borderRadius: '5px',
                marginRight: '10px'
              }}
            >
              Reload Page
            </button>
            <button 
              onClick={() => this.setState({ hasError: false, error: null })}
              style={{ 
                padding: '10px 20px', 
                background: '#4a6eb5', 
                color: 'white', 
                border: 'none', 
                borderRadius: '5px' 
              }}
            >
              Try Again
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <div className="App">
            <Suspense fallback={
              <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '100vh',
                flexDirection: 'column'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  border: '4px solid #f3f3f3',
                  borderTop: '4px solid #4a6eb5',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite'
                }}></div>
                <p style={{ marginTop: '20px' }}>Loading Security Dashboard...</p>
              </div>
            }>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/debug" element={<DebugDashboard />} />
                <Route path="/" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                <Route path="/settings" element={
                  <ProtectedRoute>
                    <HoneypotSettings />
                  </ProtectedRoute>
                } />
                <Route path="/logs" element={
                  <ProtectedRoute>
                    <LogAnalysis />
                  </ProtectedRoute>
                } />
                <Route path="/analytics" element={
                  <ProtectedRoute>
                    <Analytics />
                  </ProtectedRoute>
                } />
                <Route path="*" element={<Navigate to="/login" />} />
              </Routes>
            </Suspense>
          </div>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  )
}

export default App
