import React, { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import { useNavigate } from 'react-router-dom'
import honeypotApi from '../services/honeypotApi'
import './Dashboard.css'

const Dashboard = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [recentActivities, setRecentActivities] = useState([])
  const [loading, setLoading] = useState(true)
  const [apiStatus, setApiStatus] = useState('checking')

  useEffect(() => {
    loadDashboardData()
    
    // Set up real-time updates every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)
    
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [statsData, logsData] = await Promise.all([
        honeypotApi.getHoneypotStats(),
        honeypotApi.getHoneypotLogs()
      ])
      
      setStats(statsData)
      setRecentActivities(logsData.slice(0, 5))
      setApiStatus('connected')
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      setApiStatus('disconnected')
      // Use mock data as fallback
      setStats(honeypotApi.getMockStats())
      setRecentActivities(honeypotApi.getMockLogs().slice(0, 3))
    } finally {
      setLoading(false)
    }
  }

  const dashboardStats = [
    { 
      title: 'Total Attacks', 
      value: stats?.totalAttacks?.toLocaleString() || '0', 
      change: '+12%', 
      icon: 'fas fa-bug',
      color: '#dc3545'
    },
    { 
      title: 'Blocked IPs', 
      value: stats?.blockedIPs?.toLocaleString() || '0', 
      change: '+8%', 
      icon: 'fas fa-shield-alt',
      color: '#28a745'
    },
    { 
      title: 'Active Honeypots', 
      value: stats?.activeHoneypots?.toString() || '0', 
      change: '+2', 
      icon: 'fas fa-honey-pot',
      color: '#ffc107'
    },
    { 
      title: 'Threat Level', 
      value: stats?.threatLevel || 'Unknown', 
      change: 'Active', 
      icon: 'fas fa-exclamation-triangle',
      color: '#fd7e14'
    }
  ]

  if (loading && !stats) {
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <div className="header-content">
            <h1>Security Dashboard</h1>
            <div className="header-actions">
              <span className="welcome">Welcome, {user?.name}</span>
              <button onClick={logout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </div>
        </header>
        <div className="dashboard-content">
          <div style={{textAlign: 'center', padding: '50px'}}>
            <div className="loading-spinner"></div>
            <p>Loading honeypot data...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Security Dashboard</h1>
          <div className="header-actions">
            <span className="welcome">Welcome, {user?.name}</span>
            <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
              <span style={{
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '0.8rem',
                fontWeight: '600',
                backgroundColor: apiStatus === 'connected' ? '#28a745' : '#dc3545',
                color: 'white'
              }}>
                API: {apiStatus === 'connected' ? 'Connected' : 'Demo Mode'}
              </span>
              <button onClick={logout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        {/* Stats Grid */}
        <div className="stats-grid">
          {dashboardStats.map((stat, index) => (
            <div key={index} className="stat-card">
              <div className="stat-icon" style={{ backgroundColor: `${stat.color}20` }}>
                <i className={stat.icon} style={{ color: stat.color }}></i>
              </div>
              <div className="stat-info">
                <h3>{stat.title}</h3>
                <div className="stat-value">{stat.value}</div>
                <span className="stat-change" style={{ color: stat.color }}>
                  {stat.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="content-grid">
          {/* Recent Activity */}
          <div className="content-card">
            <div className="card-header">
              <h3>Recent Attack Attempts</h3>
              <button className="view-all" onClick={() => navigate('/logs')}>
                View All
              </button>
            </div>
            <div className="activity-list">
              {recentActivities.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-time">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </div>
                  <div className="activity-ip">{activity.ip}</div>
                  <div className="activity-type">{activity.type}</div>
                  <div className={`activity-severity severity-${activity.severity}`}>
                    {activity.severity}
                  </div>
                </div>
              ))}
              {recentActivities.length === 0 && (
                <div style={{textAlign: 'center', padding: '20px', color: '#666'}}>
                  No recent attacks detected
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="content-card">
            <div className="card-header">
              <h3>Quick Actions</h3>
            </div>
            <div className="quick-actions">
              <button className="action-btn" onClick={() => navigate('/settings')}>
                <i className="fas fa-cog"></i>
                <span>Honeypot Settings</span>
              </button>
              <button className="action-btn" onClick={() => navigate('/logs')}>
                <i className="fas fa-file-alt"></i>
                <span>View Logs</span>
              </button>
              <button className="action-btn" onClick={() => navigate('/analytics')}>
                <i className="fas fa-chart-bar"></i>
                <span>Analytics</span>
              </button>
              <button className="action-btn" onClick={() => window.location.reload()}>
                <i className="fas fa-sync-alt"></i>
                <span>Refresh Data</span>
              </button>
            </div>
          </div>

          {/* System Status */}
          <div className="content-card">
            <div className="card-header">
              <h3>Honeypot Status</h3>
            </div>
            <div className="status-list">
              <div className="status-item">
                <div className="status-info">
                  <span className="status-label">SSH Honeypot</span>
                  <span className="status-value">Running</span>
                </div>
                <div className="status-indicator running"></div>
              </div>
              <div className="status-item">
                <div className="status-info">
                  <span className="status-label">FTP Honeypot</span>
                  <span className="status-value">Running</span>
                </div>
                <div className="status-indicator running"></div>
              </div>
              <div className="status-item">
                <div className="status-info">
                  <span className="status-label">HTTP Honeypot</span>
                  <span className="status-value">Running</span>
                </div>
                <div className="status-indicator running"></div>
              </div>
              <div className="status-item">
                <div className="status-info">
                  <span className="status-label">API Connection</span>
                  <span className="status-value">{apiStatus === 'connected' ? 'Connected' : 'Demo Mode'}</span>
                </div>
                <div className={`status-indicator ${apiStatus === 'connected' ? 'running' : 'stopped'}`}></div>
              </div>
            </div>
          </div>

          {/* Threat Map */}
          <div className="content-card">
            <div className="card-header">
              <h3>Live Threat Map</h3>
            </div>
            <div className="threat-map">
              <div className="map-placeholder">
                <i className="fas fa-globe-americas"></i>
                <p>Monitoring {stats?.activeHoneypots || 0} Honeypots</p>
                <span>{stats?.totalAttacks || 0} attacks detected</span>
                {apiStatus === 'disconnected' && (
                  <div style={{marginTop: '10px', fontSize: '0.8rem', color: '#ffc107'}}>
                    Using demo data - API not connected
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
