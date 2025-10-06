import React, { useState } from 'react'

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'user'
  })

  const checkPasswordStrength = (pass) => {
    const strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
    return strongRegex.test(pass)
  }

  const handleRegister = (e) => {
    e.preventDefault()
    
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!')
      return
    }

    if (!checkPasswordStrength(formData.password)) {
      alert('Password must be 8+ characters with uppercase, lowercase, number and special character!')
      return
    }

    // In real app, send to backend
    alert('Registration successful! You can now login.')
    window.location.href = '/'
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-96">
        <h1 className="text-2xl font-bold text-white mb-6 text-center">
          📝 Register Account
        </h1>
        
        <form onSubmit={handleRegister}>
          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Username</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Role</label>
            <select
              value={formData.role}
              onChange={(e) => setFormData({...formData, role: e.target.value})}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
            >
              <option value="user">Security Analyst</option>
              <option value="admin">Administrator</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-gray-300 mb-2">Password</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              required
            />
            {formData.password && !checkPasswordStrength(formData.password) && (
              <div className="text-red-400 text-sm mt-1">
                <p>Password must contain:</p>
                <p>• 8+ characters</p>
                <p>• Uppercase & lowercase letters</p>
                <p>• At least one number</p>
                <p>• At least one special character</p>
              </div>
            )}
          </div>

          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Confirm Password</label>
            <input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              required
            />
            {formData.confirmPassword && formData.password !== formData.confirmPassword && (
              <p className="text-red-400 text-sm mt-1">Passwords do not match!</p>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-md font-semibold mb-4"
          >
            Register Account
          </button>
        </form>

        <div className="text-center">
          <button
            onClick={() => window.location.href = '/'}
            className="text-blue-400 hover:text-blue-300 text-sm"
          >
            Already have an account? Login here
          </button>
        </div>
      </div>
    </div>
  )
}

export default Register
