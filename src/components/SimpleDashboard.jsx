import React from 'react'
import { useAuth } from './AuthContext'

const SimpleDashboard = () => {
  const { user, logout } = useAuth()

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: '#f8f9fa',
      fontFamily: 'Arial, sans-serif'
    }}>
      <header style={{
        background: 'white',
        padding: '20px 30px',
        borderBottom: '1px solid #e1e5e9',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, color: '#1a2b4c' }}>Security Dashboard</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <span style={{ color: '#666' }}>Welcome, {user?.name}</span>
          <button 
            onClick={logout}
            style={{
              background: '#dc3545',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </header>

      <div style={{ padding: '30px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '20px',
          marginBottom: '30px'
        }}>
          <div style={{
            background: 'white',
            padding: '25px',
            borderRadius: '12px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
          }}>
            <h3 style={{ color: '#666', margin: '0 0 10px 0' }}>Total Attacks</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a2b4c' }}>1,247</div>
            <span style={{ color: '#dc3545', fontSize: '0.8rem', fontWeight: '600' }}>+12%</span>
          </div>
          
          <div style={{
            background: 'white',
            padding: '25px',
            borderRadius: '12px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
          }}>
            <h3 style={{ color: '#666', margin: '0 0 10px 0' }}>Active Honeypots</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a2b4c' }}>5</div>
            <span style={{ color: '#28a745', fontSize: '0.8rem', fontWeight: '600' }}>All Running</span>
          </div>
        </div>

        <div style={{
          background: 'white',
          padding: '25px',
          borderRadius: '12px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
        }}>
          <h3 style={{ margin: '0 0 20px 0', color: '#1a2b4c' }}>Quick Status</h3>
          <p>✅ API Server: Running on port 5000</p>
          <p>✅ Honeypots: 5 active</p>
          <p>✅ Authentication: Working</p>
          <p>🔧 Dashboard: Basic version loaded</p>
        </div>
      </div>
    </div>
  )
}

export default SimpleDashboard
