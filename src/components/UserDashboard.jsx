import React from 'react'
import './Dashboard.css'

const UserDashboard = () => {
  return (
    <div className="dashboard">
      <h1>Honeypot Dashboard</h1>
      
      <div className="dashboard-grid">
        {/* Main Card - Honeypot Status */}
        <div className="balance-card">
          <div className="card-title">Honeypot Status</div>
          <div className="balance-amount">Active & Monitoring</div>
          <div className="card-details">
            <div>
              <div className="system-info">All Systems Operational</div>
              <div className="uptime">Uptime: 99.8%</div>
            </div>
            <div>
              <i className="fas fa-shield-alt"></i>
            </div>
          </div>
        </div>

        {/* Stats Card */}
        <div className="stats-card">
          <div className="card-header">
            <h3>Attack Statistics</h3>
            <span className="positive">+12.5%</span>
          </div>
          <div className="stats-content">
            <div className="stat-item">
              <div className="stat-label">SSH Attacks</div>
              <div className="stat-value">1,247</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Web Attacks</div>
              <div className="stat-value">892</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Database Attacks</div>
              <div className="stat-value">431</div>
            </div>
          </div>
        </div>
      </div>

      {/* Activity Section */}
      <div className="activity-section">
        <div className="card">
          <div className="card-header">
            <h3>Recent Activity</h3>
          </div>
          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-icon ssh">SSH</div>
              <div className="activity-details">
                <div className="activity-title">SSH Brute Force Attempt</div>
                <div className="activity-meta">From: 192.168.1.105 • 2 minutes ago</div>
              </div>
              <div className="activity-status high">High</div>
            </div>
            <div className="activity-item">
              <div className="activity-icon web">WEB</div>
              <div className="activity-details">
                <div className="activity-title">SQL Injection Attempt</div>
                <div className="activity-meta">From: 10.0.2.18 • 5 minutes ago</div>
              </div>
              <div className="activity-status critical">Critical</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserDashboard
