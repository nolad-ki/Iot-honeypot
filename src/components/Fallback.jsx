import React from 'react'
import './Auth.css'

const Fallback = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <i className="fas fa-shield-alt"></i>
          <h2>Honeypot Security Dashboard</h2>
          <p>Loading application...</p>
        </div>
        <div style={{textAlign: 'center', padding: '20px'}}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #4a6eb5',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto'
          }}></div>
          <p style={{marginTop: '15px', color: '#666'}}>Initializing security dashboard...</p>
        </div>
      </div>
    </div>
  )
}

export default Fallback
