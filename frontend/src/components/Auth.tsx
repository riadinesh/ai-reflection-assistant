import { useState } from 'react'
import { API_URL } from '../config'

interface AuthProps {
  onAuthSuccess: (token: string) => void
}

export default function Auth({ onAuthSuccess }: AuthProps) {
  const [mode, setMode] = useState<'login' | 'signup'>('login')
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = mode === 'signup' ? '/signup' : '/login'
      const body = mode === 'signup'
        ? { username, email, password }
        : { username, password }

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      const data = await res.json()

      if (data.access_token) {
        onAuthSuccess(data.access_token)
      } else {
        setError(data.message || 'Something went wrong.')
      }
    } catch (err) {
      setError('Could not connect to server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">reflections</h2>
        <p className="auth-subtitle">your weekly thinking space</p>

        <div className="auth-toggle">
          <button
            className={`auth-toggle-btn ${mode === 'login' ? 'active' : ''}`}
            onClick={() => { setMode('login'); setError('') }}
          >
            log in
          </button>
          <button
            className={`auth-toggle-btn ${mode === 'signup' ? 'active' : ''}`}
            onClick={() => { setMode('signup'); setError('') }}
          >
            sign up
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label className="auth-label">username</label>
            <input
              className="auth-input"
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="your username"
            />
          </div>

          {mode === 'signup' && (
            <div className="auth-field">
              <label className="auth-label">email</label>
              <input
                className="auth-input"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="your email"
              />
            </div>
          )}

          <div className="auth-field">
            <label className="auth-label">password</label>
            <input
              className="auth-input"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button
            className="auth-submit-btn"
            type="submit"
            disabled={loading}
          >
            {loading ? 'please wait...' : mode === 'login' ? 'log in' : 'create account'}
          </button>
        </form>
      </div>
    </div>
  )
}
