import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Register from './components/Register'
import AdminDashboard from './components/AdminDashboard'
import UserDashboard from './components/UserDashboard'
import './index.css'

// Simple auth check
const isAuthenticated = () => {
  return localStorage.getItem('isLoggedIn') === 'true'
}

const getuserRole = () => {
  return localStorage.getItem('userRole') || 'user'
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={
              isAuthenticated() ? (
                getuserRole() === 'admin' ? (
                  <AdminDashboard />
                ) : (
                  <UserDashboard />
                )
              ) : (
                <Navigate to="/" />
              )
            } 
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
