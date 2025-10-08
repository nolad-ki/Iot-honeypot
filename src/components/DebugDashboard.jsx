import React, { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'

const DebugDashboard = () => {
  const { user, logout } = useAuth()
  const [error, setError] = useState(null)

  useEffect(() => {
    console.log('DebugDashboard mounted')
    console.log('User:', user)
    
    // Test if components are loading
    try {
      require('./Dashboard')
      console.log('✅ Dashboard component loaded')
    } catch (e) {
      console.error('❌ Dashboard component failed:', e)
      setError(e.toString())
    }
  }, [user])

  if (error) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial', background: '#ffebee', color: '#c62828' }}>
        <h1>🚨 Dashboard Error</h1>
        <p><strong>Error:</strong> {error}</p>
        <button onClick={() => window.location.reload()} style={{ padding: '10px 20px', background: '#c62828', color: 'white', border: 'none', borderRadius: '5px' }}>
          Reload Page
        </button>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🔧 Debug Dashboard</h1>
      <p><strong>User:</strong> {user ? JSON.stringify(user) : 'No user'}</p>
      <p><strong>Status:</strong> Components loading correctly</p>
      <button onClick={() => window.location.href = '/'} style={{ padding: '10px 20px', background: '#4a6eb5', color: 'white', border: 'none', borderRadius: '5px' }}>
        Go to Main Dashboard
      </button>
    </div>
  )
}

export default DebugDashboard
