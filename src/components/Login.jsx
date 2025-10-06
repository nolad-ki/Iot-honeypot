import React, { useState } from 'react'
import { Shield } from 'lucide-react'

const Login = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if ((username === 'admin' && password === 'admin123') || 
        (username === 'user' && password === 'user123')) {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('userRole', username === 'admin' ? 'admin' : 'user')
      localStorage.setItem('username', username)
      window.location.href = '/dashboard'
    } else {
      alert('Invalid credentials. Use admin/admin123 or user/user123')
    }
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <div className="bg-blue-600 p-3 rounded-xl">
                <Shield className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 ml-4">VertexGuard</h1>
            </div>
            <p className="text-gray-600">Security is a process, not a product</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your username"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Signing in...' : 'Sign in to Dashboard'}
            </button>
          </form>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="text-blue-900 font-semibold mb-2">Demo Credentials</h3>
            <div className="text-sm text-blue-700 space-y-1">
              <div>Administrator: admin / admin123</div>
              <div>Security Analyst: user / user123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
