import React from 'react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const AttackCharts = ({ attacks }) => {
  // Process attack data for charts
  const serviceData = [
    { name: 'FTP', value: attacks.filter(a => a.honeypot?.includes('ftp')).length, color: '#3B82F6' },
    { name: 'HTTP', value: attacks.filter(a => a.honeypot?.includes('http')).length, color: '#10B981' },
    { name: 'SSH', value: attacks.filter(a => a.honeypot?.includes('ssh')).length, color: '#F59E0B' },
    { name: 'RDP', value: attacks.filter(a => a.honeypot?.includes('rdp')).length, color: '#EF4444' },
    { name: 'MySQL', value: attacks.filter(a => a.honeypot?.includes('mysql')).length, color: '#8B5CF6' }
  ]

  const severityData = [
    { name: 'Critical', count: 2, color: '#EF4444' },
    { name: 'High', count: 5, color: '#F59E0B' },
    { name: 'Medium', count: 8, color: '#10B981' },
    { name: 'Low', count: 15, color: '#3B82F6' }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Service Distribution */}
      <div>
        <h5 className="text-sm font-medium text-gray-400 mb-4">By Service Type</h5>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={serviceData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={80}
              paddingAngle={2}
              dataKey="value"
            >
              {serviceData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex flex-wrap gap-2 mt-4 justify-center">
          {serviceData.map((service, index) => (
            <div key={index} className="flex items-center space-x-1">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: service.color }}
              ></div>
              <span className="text-xs text-gray-400">{service.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Severity Distribution */}
      <div>
        <h5 className="text-sm font-medium text-gray-400 mb-4">By Severity Level</h5>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={severityData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9CA3AF" fontSize={12} />
            <YAxis stroke="#9CA3AF" fontSize={12} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                border: '1px solid #374151',
                borderRadius: '8px'
              }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {severityData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default AttackCharts
