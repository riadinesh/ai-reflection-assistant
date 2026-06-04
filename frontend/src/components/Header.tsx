import ProfileMenu from './ProfileMenu'

interface HeaderProps {
    username: string
    email: string
    onSettings: () => void
    onLogout: () => void
}

export default function Header({ username, email, onSettings, onLogout }: HeaderProps) {
    return (
        <header className="app-header">
            <div className="app-header-brand">
                <span className="app-header-title">reflections</span>
                <span className="app-header-tagline">your weekly thinking space</span>
            </div>
            <ProfileMenu username={username} email={email} onSettings={onSettings} onLogout={onLogout} />
        </header>
    )
}
