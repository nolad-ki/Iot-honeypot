import React, { useState } from 'react'
import { Search, Filter, Download, AlertTriangle, CheckCircle, Clock } from 'lucide-react'

const LogAnalysis = ({ attacks }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedLevel, setSelectedLevel] = useState('all')

  const logLevels = {
    high: { color: 'text-red-400', bg: 'bg-red-400/10', icon: AlertTriangle },
    medium: { color: 'text-yellow-400', bg: 'bg-yellow-400/10', icon: Clock },
    low: { color: 'text-green-400', bg: 'bg-green-400/10', icon: CheckCircle }
  }

  const filteredLogs = attacks.filter(log => {
    const matchesSearch = log.details?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         log.source_ip?.includes(searchTerm) ||
                         log.type?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesLevel = selectedLevel === 'all' || log.severity === selectedLevel
    return matchesSearch && matchesLevel
  })

  const getLogLevel = (log) => {
    if (log.type?.includes('Brute Force') || log.type?.includes('Critical')) return 'high'
    if (log.type?.includes('Login') || log.type?.includes('Attempt')) return 'medium'
    return 'low'
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search logs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <select
          value={selectedLevel}
          onChange={(e) => setSelectedLevel(e.target.value)}
          className="px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">All Levels</option>
          <option value="high">High Severity</option>
          <option value="medium">Medium Severity</option>
          <option value="low">Low Severity</option>
        </select>

        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center space-x-2 transition-colors">
          <Download className="h-4 w-4" />
          <span>Export</span>
        </button>
      </div>

      {/* Log List */}
      <div className="bg-gray-700 rounded-lg border border-gray-600 max-h-96 overflow-y-auto">
        {filteredLogs.length > 0 ? (
          filteredLogs.map((log, index) => {
            const level = getLogLevel(log)
            const LevelIcon = logLevels[level].icon
            
            return (
              <div
                key={index}
                className="p-4 border-b border-gray-600 last:border-b-0 hover:bg-gray-600/50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    <div className={`p-2 rounded-lg ${logLevels[level].bg}`}>
                      <LevelIcon className={`h-4 w-4 ${logLevels[level].color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-semibold text-white text-sm">{log.type}</span>
                        <span className={`text-xs px-2 py-1 rounded-full ${logLevels[level].bg} ${logLevels[level].color}`}>
                          {level.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm mb-1">{log.details}</p>
                      <div className="flex items-center space-x-4 text-xs text-gray-400">
                        <span>Source: {log.source_ip}</span>
                        <span>Service: {log.honeypot}</span>
                        <span>{new Date(log.timestamp).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )
          })
        ) : (
          <div className="p-8 text-center text-gray-400">
            <Filter className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No logs match your current filters</p>
            <p className="text-sm">Try adjusting your search criteria</p>
          </div>
        )}
      </div>

      {/* Summary */}
      <div className="flex items-center justify-between text-sm text-gray-400">
        <span>Showing {filteredLogs.length} of {attacks.length} total logs</span>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-red-400 rounded-full"></div>
            <span>High: {attacks.filter(l => getLogLevel(l) === 'high').length}</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
            <span>Medium: {attacks.filter(l => getLogLevel(l) === 'medium').length}</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span>Low: {attacks.filter(l => getLogLevel(l) === 'low').length}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LogAnalysis
