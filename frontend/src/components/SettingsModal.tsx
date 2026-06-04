import { useState, useEffect } from 'react'
import { API_URL } from '../config'

interface SettingsModalProps {
    username: string
    email: string
    onClose: () => void
    onSaved: (user: { username: string; email: string }) => void
}

export default function SettingsModal({ username, email, onClose, onSaved }: SettingsModalProps) {
    const [newUsername, setNewUsername] = useState(username)
    const [newEmail, setNewEmail] = useState(email)

    // Close on Escape
    useEffect(() => {
        const onKey = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose()
        }
        window.addEventListener('keydown', onKey)
        return () => window.removeEventListener('keydown', onKey)
    }, [onClose])

    function handleSave(e: React.FormEvent<HTMLFormElement>) {
        fetch(`${API_URL}/settings`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`},
            body: JSON.stringify({ username: newUsername, email: newEmail })
        })
        e.preventDefault()
        onSaved({ username: newUsername, email: newEmail })
        onClose()
    }

    return (
        // Clicking the dimmed backdrop closes the modal
        <div className="settings-overlay" onClick={onClose}>
            {/* stopPropagation so clicks inside the card don't close it */}
            <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
                <button className="settings-close-btn" onClick={onClose} aria-label="close">×</button>
                <h2 className="settings-title">settings</h2>

                <form className="settings-form" onSubmit={handleSave}>
                    <div className="settings-field">
                        <label className="settings-label">username</label>
                        <input
                            className="settings-input"
                            type="text"
                            value={newUsername}
                            onChange={(e) => setNewUsername(e.target.value)}
                        />
                    </div>

                    <div className="settings-field">
                        <label className="settings-label">email</label>
                        <input
                            className="settings-input"
                            type="email"
                            value={newEmail}
                            onChange={(e) => setNewEmail(e.target.value)}
                        />
                    </div>

                    <button className="settings-save-btn" type="submit">save changes</button>
                </form>
            </div>
        </div>
    )
}
