import React from 'react'
import { Globe } from 'lucide-react'

const ThreatMap = ({ attacks }) => {
  // Mock threat locations
  const threatLocations = [
    { city: 'New York', country: 'USA', count: 12, lat: 40.7128, lng: -74.0060 },
    { city: 'London', country: 'UK', count: 8, lat: 51.5074, lng: -0.1278 },
    { city: 'Tokyo', country: 'Japan', count: 15, lat: 35.6762, lng: 139.6503 },
    { city: 'Moscow', country: 'Russia', count: 6, lat: 55.7558, lng: 37.6173 },
    { city: 'Singapore', country: 'Singapore', count: 9, lat: 1.3521, lng: 103.8198 },
    { city: 'São Paulo', country: 'Brazil', count: 5, lat: -23.5505, lng: -46.6333 }
  ]

  const getThreatSize = (count) => {
    if (count > 10) return 'w-8 h-8'
    if (count > 5) return 'w-6 h-6'
    return 'w-4 h-4'
  }

  const getThreatColor = (count) => {
    if (count > 10) return 'bg-red-500'
    if (count > 5) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  return (
    <div className="relative">
      {/* Simplified World Map Visualization */}
      <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
        <div className="relative h-64 bg-gradient-to-br from-blue-900/30 to-gray-800/30 rounded-lg overflow-hidden">
          {/* Mock map background */}
          <div className="absolute inset-0 opacity-20">
            <div className="flex items-center justify-center h-full">
              <Globe className="h-32 w-32 text-gray-600" />
            </div>
          </div>
          
          {/* Threat indicators */}
          {threatLocations.map((location, index) => (
            <div
              key={index}
              className={`absolute ${getThreatSize(location.count)} ${getThreatColor(location.count)} rounded-full border-2 border-white animate-pulse`}
              style={{
                left: `${50 + (location.lng / 360) * 40}%`,
                top: `${50 - (location.lat / 180) * 40}%`,
              }}
            >
              <div className="relative group">
                <div className="w-full h-full rounded-full"></div>
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block">
                  <div className="bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                    {location.city}: {location.count} threats
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Threat Legend */}
      <div className="mt-4 flex justify-center space-x-6">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-400">High (10+)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-400">Medium (5-10)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span className="text-xs text-gray-400">Low (under 5)</span>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="mt-4 space-y-2">
        <h5 className="text-sm font-medium text-gray-400">Recent Global Activity</h5>
        {threatLocations.slice(0, 3).map((location, index) => (
          <div key={index} className="flex items-center justify-between text-xs">
            <span className="text-gray-300">{location.city}, {location.country}</span>
            <span className="text-red-400">{location.count} attacks</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ThreatMap
