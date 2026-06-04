import { useState } from 'react'
import './App.css'
import GoalsSidebar from './components/GoalsSidebar'
import ReflectionPanel from './components/ReflectionPanel'
import Auth from './components/Auth'
import Header from './components/Header'

// Read the username out of the JWT (client-side only, no API call).
function getUsername(token: string | null): string {
  if (!token) return ''
  try {
    return JSON.parse(atob(token.split('.')[1])).sub ?? ''
  } catch {
    return ''
  }
}

function App() {
  const [token, setToken] = useState<string | null>(null)

  function handleAuthSuccess(t: string) {
    localStorage.setItem('token', t)
    setToken(t)
  }

  function handleLogout() {
    localStorage.removeItem('token')
    setToken(null)
  }

  if (!token) {
    return <Auth onAuthSuccess={handleAuthSuccess} />
  }

  return (
    <div>
      {/* TODO: replace email placeholder with real data from your /me endpoint */}
      <Header username={getUsername(token)} email="your email" onLogout={handleLogout} />
      <GoalsSidebar />
      <ReflectionPanel/>
    </div>
  )
}

export default App
