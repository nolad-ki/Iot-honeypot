import React, { useState } from 'react'
import { useAuth } from './AuthContext'
import './Settings.css'

const HoneypotSettings = () => {
  const { user, logout } = useAuth()
  const [settings, setSettings] = useState({
    honeypotName: 'Production Honeypot',
    honeypotType: 'medium',
    logLevel: 'detailed',
    autoBlock: true,
    emailAlerts: true,
    slackAlerts: false,
    maxConnections: 100,
    ports: '22,80,443,3389,5900',
    responseDelay: 2,
    fakeServices: ['ssh', 'http', 'ftp', 'mysql']
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleServiceToggle = (service) => {
    setSettings(prev => ({
      ...prev,
      fakeServices: prev.fakeServices.includes(service)
        ? prev.fakeServices.filter(s => s !== service)
        : [...prev.fakeServices, service]
    }))
  }

  const handleSave = () => {
    // Simulate API call
    alert('Settings saved successfully!')
  }

  const serviceOptions = [
    { id: 'ssh', name: 'SSH Server', description: 'Fake SSH service' },
    { id: 'http', name: 'Web Server', description: 'Fake HTTP service' },
    { id: 'ftp', name: 'FTP Server', description: 'Fake FTP service' },
    { id: 'mysql', name: 'MySQL Database', description: 'Fake MySQL service' },
    { id: 'rdp', name: 'Remote Desktop', description: 'Fake RDP service' },
    { id: 'telnet', name: 'Telnet', description: 'Fake Telnet service' }
  ]

  return (
    <div className="settings-page">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Honeypot Settings</h1>
          <div className="header-actions">
            <span className="welcome">Welcome, {user?.name}</span>
            <button onClick={logout} className="logout-btn">
              <i className="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        </div>
      </header>

      <div className="settings-content">
        <div className="settings-grid">
          {/* Basic Settings */}
          <div className="settings-section">
            <h3>Basic Configuration</h3>
            <div className="settings-group">
              <div className="form-group">
                <label>Honeypot Name</label>
                <input
                  type="text"
                  name="honeypotName"
                  value={settings.honeypotName}
                  onChange={handleChange}
                />
              </div>
              
              <div className="form-group">
                <label>Honeypot Type</label>
                <select 
                  name="honeypotType" 
                  value={settings.honeypotType}
                  onChange={handleChange}
                >
                  <option value="low">Low Interaction</option>
                  <option value="medium">Medium Interaction</option>
                  <option value="high">High Interaction</option>
                </select>
              </div>

              <div className="form-group">
                <label>Log Level</label>
                <select 
                  name="logLevel" 
                  value={settings.logLevel}
                  onChange={handleChange}
                >
                  <option value="minimal">Minimal</option>
                  <option value="normal">Normal</option>
                  <option value="detailed">Detailed</option>
                </select>
              </div>
            </div>
          </div>

          {/* Network Settings */}
          <div className="settings-section">
            <h3>Network Configuration</h3>
            <div className="settings-group">
              <div className="form-group">
                <label>Ports to Monitor</label>
                <input
                  type="text"
                  name="ports"
                  value={settings.ports}
                  onChange={handleChange}
                  placeholder="e.g., 22,80,443,3389"
                />
                <small>Comma-separated list of ports</small>
              </div>
              
              <div className="form-group">
                <label>Max Concurrent Connections</label>
                <input
                  type="number"
                  name="maxConnections"
                  value={settings.maxConnections}
                  onChange={handleChange}
                  min="1"
                  max="1000"
                />
              </div>

              <div className="form-group">
                <label>Response Delay (seconds)</label>
                <input
                  type="number"
                  name="responseDelay"
                  value={settings.responseDelay}
                  onChange={handleChange}
                  min="0"
                  max="10"
                  step="0.5"
                />
              </div>
            </div>
          </div>

          {/* Fake Services */}
          <div className="settings-section">
            <h3>Fake Services</h3>
            <div className="services-grid">
              {serviceOptions.map(service => (
                <div key={service.id} className="service-card">
                  <div className="service-info">
                    <h4>{service.name}</h4>
                    <p>{service.description}</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={settings.fakeServices.includes(service.id)}
                      onChange={() => handleServiceToggle(service.id)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Alert Settings */}
          <div className="settings-section">
            <h3>Alert Settings</h3>
            <div className="settings-group">
              <div className="checkbox-group">
                <label className="checkbox">
                  <input
                    type="checkbox"
                    name="autoBlock"
                    checked={settings.autoBlock}
                    onChange={handleChange}
                  />
                  <span>Automatically block suspicious IPs</span>
                </label>
              </div>

              <div className="checkbox-group">
                <label className="checkbox">
                  <input
                    type="checkbox"
                    name="emailAlerts"
                    checked={settings.emailAlerts}
                    onChange={handleChange}
                  />
                  <span>Enable email alerts</span>
                </label>
              </div>

              <div className="checkbox-group">
                <label className="checkbox">
                  <input
                    type="checkbox"
                    name="slackAlerts"
                    checked={settings.slackAlerts}
                    onChange={handleChange}
                  />
                  <span>Enable Slack notifications</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="settings-actions">
          <button className="btn-secondary">Reset to Defaults</button>
          <button className="btn-primary" onClick={handleSave}>
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}

export default HoneypotSettings
