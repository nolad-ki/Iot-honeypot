import React, { useState, useEffect } from 'react'
import { honeypotAPI } from '../lib/honeypot-api'

const UserDashboard = () => {
  const [stats, setStats] = useState({})
  const [attacks, setAttacks] = useState([])

  useEffect(() => {
    const loadData = async () => {
      const [attacksData, statsData] = await Promise.all([
        honeypotAPI.getAttacks(),
        honeypotAPI.getStats()
      ])
      setAttacks(attacksData)
      setStats(statsData)
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
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">🔍 Security Analyst Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-md"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-lg">
            <h3 className="text-gray-400">Active Threats</h3>
            <p className="text-3xl font-bold text-red-400">{stats.attacksToday || 0}</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg">
            <h3 className="text-gray-400">Honeypots</h3>
            <p className="text-3xl font-bold text-green-400">{stats.honeypotsActive || 5}</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg">
            <h3 className="text-gray-400">Threat Level</h3>
            <p className="text-3xl font-bold text-yellow-400">{stats.threatLevel || 'Low'}</p>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">Recent Attack Activity</h2>
          <div className="space-y-3">
            {attacks.length > 0 ? (
              attacks.map((attack, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded">
                  <div className="flex justify-between">
                    <span className="font-semibold">{attack.type}</span>
                    <span className="text-gray-400 text-sm">
                      {new Date(attack.timestamp).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-gray-300 text-sm mt-1">{attack.details}</p>
                  <p className="text-blue-400 text-sm">Source: {attack.source_ip}</p>
                </div>
              ))
            ) : (
              <div className="text-center text-gray-500 py-8">
                Monitoring for attacks... No activity detected yet.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserDashboard
