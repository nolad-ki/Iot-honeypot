import React, { useState, useEffect } from 'react'
import { Shield, LogOut, Bell, Activity, Globe, Server, AlertTriangle, Cpu } from 'lucide-react'
import { honeypotAPI } from '../lib/honeypot-api'

const AdminDashboard = () => {
  const [stats, setStats] = useState({})
  const [attacks, setAttacks] = useState([])
  const [honeypotStatus, setHoneypotStatus] = useState([])

  useEffect(() => {
    const loadData = async () => {
      const [attacksData, statsData] = await Promise.all([
        honeypotAPI.getAttacks(),
        honeypotAPI.getStats()
      ])
      setAttacks(attacksData)
      setStats(statsData)
      
      // Mock honeypot status
      setHoneypotStatus([
        { name: 'FTP Honeypot', status: 'active', attacks: attacksData.filter(a => a.honeypot?.includes('ftp')).length },
        { name: 'HTTP Honeypot', status: 'active', attacks: attacksData.filter(a => a.honeypot?.includes('http')).length },
        { name: 'SSH Honeypot', status: 'active', attacks: attacksData.filter(a => a.honeypot?.includes('ssh')).length },
        { name: 'RDP Honeypot', status: 'active', attacks: attacksData.filter(a => a.honeypot?.includes('rdp')).length },
        { name: 'MySQL Honeypot', status: 'active', attacks: attacksData.filter(a => a.honeypot?.includes('mysql')).length }
      ])
    }

    loadData()
    const interval = setInterval(loadData, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleLogout = () => {
    localStorage.clear()
    window.location.href = '/'
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Shield className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">IoT Honeypot Dashboard</h1>
              <div className="flex items-center space-x-4 mt-2">
                <h2 className="text-lg">Welcome! Security Admin</h2>
                <span className="text-gray-400">Monitoring 5 deception systems</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-gray-700 rounded-lg relative">
              <Bell className="h-5 w-5" />
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                {stats.attacksToday || 0}
              </span>
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
            >
              <LogOut className="h-4 w-4" />
              <span>Log Out</span>
            </button>
          </div>
        </div>

        {/* Current Status */}
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">System Status</h3>
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-gray-700 p-4 rounded-lg border border-blue-500">
              <h4 className="font-semibold text-blue-400">Total Attacks</h4>
              <p className="text-2xl font-bold mt-2">{stats.totalAttacks || 0}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg border border-green-500">
              <h4 className="font-semibold text-green-400">Active Honeypots</h4>
              <p className="text-2xl font-bold mt-2">{stats.honeypotsActive || 5}/5</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg border border-yellow-500">
              <h4 className="font-semibold text-yellow-400">Today's Threats</h4>
              <p className="text-2xl font-bold mt-2">{stats.attacksToday || 0}</p>
            </div>
            <div className="bg-gray-700 p-4 rounded-lg border border-purple-500">
              <h4 className="font-semibold text-purple-400">Unique Attackers</h4>
              <p className="text-2xl font-bold mt-2">{stats.uniqueAttackers || 0}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Attack Overview */}
        <div className="lg:col-span-2 space-y-6">
          {/* Attack Summary */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Attack Summary</h3>
            <p className="text-gray-300 mb-4">Real-time monitoring of all honeypot activities.</p>
            
            <div className="space-y-3">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-semibold">
                Generate Security Report
              </button>
              
              <div className="bg-blue-900/30 p-4 rounded-lg border border-blue-700">
                <p className="text-blue-300">Live attack data from 5 IoT honeypots</p>
                <div className="mt-2 flex space-x-4">
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-xs text-gray-400">High Severity</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                    <span className="text-xs text-gray-400">Medium Severity</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-xs text-gray-400">Low Severity</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Attacks */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Recent Attack Logs</h3>
            
            {/* Quick Stats */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="text-center p-3 bg-gray-700 rounded">
                <div className="text-2xl font-bold text-red-400">{attacks.filter(a => a.severity === 'high').length}</div>
                <div className="text-sm text-gray-400">Critical</div>
              </div>
              <div className="text-center p-3 bg-gray-700 rounded">
                <div className="text-2xl font-bold text-yellow-400">{attacks.filter(a => a.severity === 'medium').length}</div>
                <div className="text-sm text-gray-400">Warnings</div>
              </div>
              <div className="text-center p-3 bg-gray-700 rounded">
                <div className="text-2xl font-bold text-green-400">{attacks.filter(a => a.severity === 'low').length}</div>
                <div className="text-sm text-gray-400">Normal</div>
              </div>
            </div>

            {/* Attack Table */}
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b border-gray-600">
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Time</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Service</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Source IP</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Attack Type</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Severity</th>
                  </tr>
                </thead>
                <tbody>
                  {attacks.slice(0, 5).map((attack, index) => (
                    <tr key={index} className="border-b border-gray-700 hover:bg-gray-700/50">
                      <td className="py-3 px-4 text-gray-300">
                        {new Date(attack.timestamp).toLocaleTimeString()}
                      </td>
                      <td className="py-3 px-4 text-gray-300">
                        <div className="flex items-center space-x-2">
                          <Server className="h-4 w-4 text-blue-400" />
                          <span>{attack.honeypot}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-300 font-mono text-sm">
                        {attack.source_ip}
                      </td>
                      <td className="py-3 px-4 text-gray-300">{attack.type}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          attack.severity === 'high' 
                            ? 'bg-red-500 text-white' 
                            : attack.severity === 'medium'
                            ? 'bg-yellow-500 text-black'
                            : 'bg-green-500 text-white'
                        }`}>
                          {attack.severity || 'low'}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {attacks.length === 0 && (
                    <tr>
                      <td colSpan="5" className="py-8 text-center text-gray-500">
                        <Activity className="h-12 w-12 mx-auto mb-2 opacity-50" />
                        <p>No attacks detected yet. Monitoring active...</p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Attack by Service */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Attacks by Service</h3>
            <div className="space-y-3">
              {honeypotStatus.map((honeypot, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg border border-gray-600">
                  <div className="flex items-center space-x-3">
                    <Cpu className="h-5 w-5 text-blue-400" />
                    <div>
                      <span className="font-semibold text-white">{honeypot.name}</span>
                      <div className="text-xs text-gray-400">{honeypot.attacks} attacks</div>
                    </div>
                  </div>
                  <span className="text-green-400 text-sm">Active</span>
                </div>
              ))}
            </div>
          </div>

          {/* Threat Level Distribution */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Threat Levels</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-red-900/20 border border-red-700 rounded">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5 text-red-400" />
                  <span className="font-semibold text-red-400">Critical Threats</span>
                </div>
                <span className="text-red-400 font-bold">{attacks.filter(a => a.severity === 'high').length}</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-yellow-900/20 border border-yellow-700 rounded">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5 text-yellow-400" />
                  <span className="font-semibold text-yellow-400">Suspicious Activity</span>
                </div>
                <span className="text-yellow-400 font-bold">{attacks.filter(a => a.severity === 'medium').length}</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-900/20 border border-green-700 rounded">
                <div className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-green-400" />
                  <span className="font-semibold text-green-400">Normal Traffic</span>
                </div>
                <span className="text-green-400 font-bold">{attacks.filter(a => a.severity === 'low').length}</span>
              </div>
            </div>
          </div>

          {/* Global Activity */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-semibold mb-4">Global Activity</h3>
            <div className="text-center p-4 bg-gray-700 rounded-lg">
              <Globe className="h-12 w-12 text-blue-400 mx-auto mb-3" />
              <p className="text-gray-300">Monitoring attacks worldwide</p>
              <div className="mt-2 text-sm text-gray-400">
                {attacks.length} total events detected
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
