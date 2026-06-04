import { useState, useRef, useEffect } from 'react'

interface ProfileMenuProps {
    username: string
    email: string
    onSettings: () => void
    onLogout: () => void
}

export default function ProfileMenu({ username, email, onSettings, onLogout }: ProfileMenuProps) {
    const [open, setOpen] = useState(false)
    const menuRef = useRef<HTMLDivElement>(null)

    // close the dropdown when clicking outside of it
    useEffect(() => {
        const handleClick = (e: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
                setOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClick)
        return () => document.removeEventListener('mousedown', handleClick)
    }, [])

    return (
        <div className="profile-menu" ref={menuRef}>
            <button className="profile-icon" onClick={() => setOpen(o => !o)} aria-label="profile">
                {/* person glyph */}
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">
                    <path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0 2c-4.42 0-8 2.69-8 6v1a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-1c0-3.31-3.58-6-8-6Z" />
                </svg>
            </button>

            {open && (
                <div className="profile-dropdown">
                    <div className="profile-info">
                        <div className="profile-username">{username}</div>
                        <div className="profile-email">{email}</div>
                    </div>
                    <div className="profile-divider" />
                    <button className="profile-dropdown-item" onClick={() => { setOpen(false); onSettings() }}>Settings</button>
                    <div className="profile-divider" />
                    <button className="profile-dropdown-item" onClick={onLogout}>Logout</button>
                </div>
            )}
        </div>
    )
}
