import { useState, useEffect } from 'react'
import './App.css'
import GoalsSidebar from './components/GoalsSidebar'
import ReflectionPanel from './components/ReflectionPanel'
import Auth from './components/Auth'
import Header from './components/Header'
import SettingsModal from './components/SettingsModal'
import { API_URL } from './config'

type User = { username: string, email: string }

function App() {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [showSettings, setShowSettings] = useState(false)

  function handleAuthSuccess(t: string) {
    localStorage.setItem('token', t)
    setToken(t)
  }

  function handleLogout() {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  function handleSettings() {
    setShowSettings(true)
  }

  function handleRevisitPastReflections() {
    // TODO: open the past reflections modal
  }

  // Fetch the logged-in user's profile (username + email) once we have a token.
  useEffect(() => {
    if (!token) return
    fetch(`${API_URL}/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(() => {})
  }, [token])

  if (!token) {
    return <Auth onAuthSuccess={handleAuthSuccess} />
  }

  return (
    <div>
      <Header username={user?.username ?? ""} email={user?.email ?? ""} onSettings={handleSettings} onLogout={handleLogout} />
      <GoalsSidebar />
      <ReflectionPanel/>
      <button className="past-reflections-btn" onClick={handleRevisitPastReflections}>
        revisit past reflections
      </button>
      {showSettings && (
        <SettingsModal
          username={user?.username ?? ""}
          email={user?.email ?? ""}
          onClose={() => setShowSettings(false)}
          onSaved={({ username, email }) => setUser({ username, email })}
        />
      )}
    </div>
  )
}

export default App
