import React, { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import honeypotApi from '../services/honeypotApi'
import './Analytics.css'

const Analytics = () => {
  const { user, logout } = useAuth()
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      setLoading(true)
      const analyticsData = await honeypotApi.getAttackAnalytics()
      setAnalytics(analyticsData)
    } catch (error) {
      console.error('Failed to load analytics:', error)
      setAnalytics(honeypotApi.getMockAnalytics())
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="analytics">
        <header className="dashboard-header">
          <div className="header-content">
            <h1>Security Analytics</h1>
            <div className="header-actions">
              <span className="welcome">Welcome, {user?.name}</span>
              <button onClick={logout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </div>
        </header>
        <div className="analytics-content">
          <div style={{textAlign: 'center', padding: '50px'}}>
            <div className="loading-spinner"></div>
            <p>Loading analytics data...</p>
          </div>
        </div>
      </div>
    )
  }

  const maxAttacks = Math.max(...analytics.timeline.map(d => d.attacks))

  return (
    <div className="analytics">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Security Analytics</h1>
          <div className="header-actions">
            <span className="welcome">Welcome, {user?.name}</span>
            <button onClick={logout} className="logout-btn">
              <i className="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        </div>
      </header>

      <div className="analytics-content">
        {/* Key Metrics */}
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon total-attacks">
              <i className="fas fa-bug"></i>
            </div>
            <div className="metric-info">
              <h3>Total Attacks</h3>
              <div className="metric-value">{analytics.totalAttacks.toLocaleString()}</div>
              <div className="metric-change up">+12% from yesterday</div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon blocked">
              <i className="fas fa-shield-alt"></i>
            </div>
            <div className="metric-info">
              <h3>Successfully Blocked</h3>
              <div className="metric-value">
                {Math.round((analytics.blockedAttacks / analytics.totalAttacks) * 100)}%
              </div>
              <div className="metric-change up">+2.1% improvement</div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon response">
              <i className="fas fa-clock"></i>
            </div>
            <div className="metric-info">
              <h3>Avg Response Time</h3>
              <div className="metric-value">2.3s</div>
              <div className="metric-change down">-0.4s faster</div>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon threats">
              <i className="fas fa-exclamation-triangle"></i>
            </div>
            <div className="metric-info">
              <h3>Active Threats</h3>
              <div className="metric-value">{analytics.uniqueAttackers}</div>
              <div className="metric-change up">+3 new</div>
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Attack Timeline */}
          <div className="chart-card">
            <div className="chart-header">
              <h3>Attack Timeline (Last 24 Hours)</h3>
              <div className="chart-legend">
                <span className="legend-item">
                  <div className="legend-color attacks"></div>
                  Attack Attempts
                </span>
              </div>
            </div>
            <div className="chart-container">
              <div className="bar-chart">
                {analytics.timeline.map((data, index) => (
                  <div key={index} className="bar-container">
                    <div 
                      className="bar" 
                      style={{ 
                        height: `${(data.attacks / maxAttacks) * 100}%`,
                        backgroundColor: '#4a6eb5'
                      }}
                      title={`${data.attacks} attacks at ${data.hour}`}
                    ></div>
                    <span className="bar-label">{data.hour}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Attack Types */}
          <div className="chart-card">
            <div className="chart-header">
              <h3>Attack Type Distribution</h3>
            </div>
            <div className="chart-container">
              <div className="pie-chart">
                {analytics.attackTypes.map((type, index) => (
                  <div key={index} className="pie-segment">
                    <div 
                      className="segment" 
                      style={{
                        backgroundColor: getSegmentColor(index),
                      }}
                    ></div>
                    <div className="segment-info">
                      <div className="segment-label">
                        <div 
                          className="color-dot" 
                          style={{ backgroundColor: getSegmentColor(index) }}
                        ></div>
                        {type.type}
                      </div>
                      <div className="segment-value">{type.count} ({type.percentage}%)</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Helper functions for pie chart
function getSegmentColor(index) {
  const colors = ['#4a6eb5', '#dc3545', '#fd7e14', '#ffc107', '#28a745', '#6c757d']
  return colors[index % colors.length]
}

export default Analytics
