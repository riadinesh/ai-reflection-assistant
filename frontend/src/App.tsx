import { useState } from 'react'
import './App.css'
import GoalsSidebar from './components/GoalsSidebar'
import ReflectionPanel from './components/ReflectionPanel'
import Auth from './components/Auth'

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
      <GoalsSidebar />
      <ReflectionPanel/>
      <button className="logout-btn" onClick={handleLogout}>log out</button>
    </div>
  )
}

export default App
