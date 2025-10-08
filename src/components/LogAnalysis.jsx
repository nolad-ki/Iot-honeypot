import React, { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import honeypotApi from '../services/honeypotApi'
import './LogAnalysis.css'

const LogAnalysis = () => {
  const { user, logout } = useAuth()
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadLogs()
  }, [])

  const loadLogs = async () => {
    try {
      setLoading(true)
      const logsData = await honeypotApi.getHoneypotLogs()
      setLogs(logsData)
    } catch (error) {
      console.error('Failed to load logs:', error)
      // Fallback to mock data
      setLogs(honeypotApi.getMockLogs())
    } finally {
      setLoading(false)
    }
  }

  const filteredLogs = logs.filter(log => {
    const matchesFilter = filter === 'all' || log.severity === filter
    const matchesSearch = log.ip.includes(searchTerm) || 
                         log.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.payload.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesFilter && matchesSearch
  })

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return 'fas fa-skull-crossbones'
      case 'high': return 'fas fa-exclamation-triangle'
      case 'medium': return 'fas fa-exclamation-circle'
      default: return 'fas fa-info-circle'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'blocked': return '#28a745'
      case 'monitored': return '#ffc107'
      default: return '#6c757d'
    }
  }

  if (loading) {
    return (
      <div className="log-analysis">
        <header className="dashboard-header">
          <div className="header-content">
            <h1>Log Analysis</h1>
            <div className="header-actions">
              <span className="welcome">Welcome, {user?.name}</span>
              <button onClick={logout} className="logout-btn">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </div>
        </header>
        <div className="log-content">
          <div style={{textAlign: 'center', padding: '50px'}}>
            <div className="loading-spinner"></div>
            <p>Loading attack logs...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="log-analysis">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Log Analysis</h1>
          <div className="header-actions">
            <span className="welcome">Welcome, {user?.name}</span>
            <button onClick={logout} className="logout-btn">
              <i className="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        </div>
      </header>

      <div className="log-content">
        {/* Filters and Search */}
        <div className="log-controls">
          <div className="search-box">
            <i className="fas fa-search"></i>
            <input
              type="text"
              placeholder="Search logs by IP, type, or payload..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'active' : ''}
              onClick={() => setFilter('all')}
            >
              All Logs
            </button>
            <button 
              className={filter === 'critical' ? 'active' : ''}
              onClick={() => setFilter('critical')}
            >
              Critical
            </button>
            <button 
              className={filter === 'high' ? 'active' : ''}
              onClick={() => setFilter('high')}
            >
              High
            </button>
            <button 
              className={filter === 'medium' ? 'active' : ''}
              onClick={() => setFilter('medium')}
            >
              Medium
            </button>
          </div>
        </div>

        {/* Logs Table */}
        <div className="logs-table-container">
          <table className="logs-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>IP Address</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Honeypot</th>
                <th>Payload</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map(log => (
                <tr key={log.id} className={`severity-${log.severity}`}>
                  <td className="timestamp">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="ip-address">
                    <i className="fas fa-desktop"></i>
                    {log.ip}
                  </td>
                  <td className="log-type">{log.type}</td>
                  <td className="severity">
                    <i className={getSeverityIcon(log.severity)}></i>
                    <span>{log.severity}</span>
                  </td>
                  <td className="honeypot">
                    <i className="fas fa-honey-pot"></i>
                    {log.honeypot}
                  </td>
                  <td className="payload" title={log.payload}>
                    {log.payload.length > 50 ? log.payload.substring(0, 50) + '...' : log.payload}
                  </td>
                  <td className="status">
                    <span style={{ color: getStatusColor(log.status) }}>
                      {log.status}
                    </span>
                  </td>
                  <td className="actions">
                    <button className="action-btn view" title="View Details">
                      <i className="fas fa-eye"></i>
                    </button>
                    <button className="action-btn block" title="Block IP">
                      <i className="fas fa-ban"></i>
                    </button>
                    <button className="action-btn export" title="Export">
                      <i className="fas fa-download"></i>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Statistics */}
        <div className="log-stats">
          <div className="stat-item">
            <div className="stat-value">{logs.length}</div>
            <div className="stat-label">Total Logs</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{logs.filter(l => l.severity === 'critical').length}</div>
            <div className="stat-label">Critical</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{logs.filter(l => l.severity === 'high').length}</div>
            <div className="stat-label">High</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{logs.filter(l => l.status === 'blocked').length}</div>
            <div className="stat-label">Blocked</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LogAnalysis
