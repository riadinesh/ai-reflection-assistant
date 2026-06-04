import { useEffect } from 'react'
import type { Summary } from '../types/Summary'

interface SummaryModalProps {
    summary: Summary
    onClose: () => void
}

export default function SummaryModal({ summary, onClose }: SummaryModalProps) {
    // Close on Escape key
    useEffect(() => {
        const onKey = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose()
        }
        window.addEventListener('keydown', onKey)
        return () => window.removeEventListener('keydown', onKey)
    }, [onClose])

    return (
        // Clicking the dimmed backdrop closes the modal
        <div className="summary-overlay" onClick={onClose}>
            {/* stopPropagation so clicks inside the card don't close it */}
            <div className="summary-modal" onClick={(e) => e.stopPropagation()}>
                <button className="summary-close-btn" onClick={onClose} aria-label="close">×</button>

                <h2 className="summary-title">your weekly reflection summary</h2>
                <p className="summary-dates">{summary.week_start} – {summary.week_end}</p>

                <p className="summary-text">{summary.summary_text}</p>

                {summary.goals_worked_on.length > 0 && (
                    <div className="summary-section">
                        <h3 className="summary-subtitle">goals worked on</h3>
                        <ul className="summary-bullets">
                            {summary.goals_worked_on.map((g, i) => <li key={i}>{g}</li>)}
                        </ul>
                    </div>
                )}

                {summary.next_steps.length > 0 && (
                    <div className="summary-section">
                        <h3 className="summary-subtitle">next steps</h3>
                        <ul className="summary-bullets">
                            {summary.next_steps.map((s, i) => <li key={i}>{s}</li>)}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    )
}
