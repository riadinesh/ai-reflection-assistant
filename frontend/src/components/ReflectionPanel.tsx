import { useState } from 'react'
import { reflectionActions } from '../hooks/ReflectionActions'
import { API_URL } from '../config'

export default function ReflectionPanel() {
    const { days, reflectionMap, dateRangeLabel, handleContentChange, handleKeyPress, goToPreviousWeek, goToNextWeek, isCurrentWeek } = reflectionActions()
    const [summarizing, setSummarizing] = useState(false)
    const [sentTo, setSentTo] = useState<string | null>(null)

    async function handleGenerateSummary() {
        setSummarizing(true)
        setSentTo(null)
        try {
            const res = await fetch(`${API_URL}/summarize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            const data = await res.json()
            setSentTo(data.email_sent_to)
        } finally {
            setSummarizing(false)
        }
    }

    return (
        <div className="reflection-panel">
            <div className="reflection-header-container">
                <h3 className="reflection-header">This Week's Reflections</h3>
                <div className="reflection-week-nav">
                    <span className="week-range-label">{dateRangeLabel}</span>
                    <div className="reflection-week-nav-btns">
                        <button className="week-nav-btn" onClick={goToPreviousWeek}>{"<"}</button>
                        {/* if on current week, disable next week button */}
                        <button className="week-nav-btn" onClick={goToNextWeek} disabled={isCurrentWeek}>{">"}</button>
                    </div>
                </div>
            </div>
            <ul className="reflection-list">
                {days.map(day => (
                    <li key={day} className="reflection-li">
                        <span className="day-label">{day}</span>
                        <textarea
                            className="reflection-input"
                            placeholder="write your reflection..."
                            value={reflectionMap[day]?.content ?? ""}
                            onChange={(e) => handleContentChange(day, e)}
                            onKeyDown={(e) => handleKeyPress(day, e)}
                        />
                    </li>
                ))}
            </ul>
            <div className="reflection-footer">
                <button className="generate-summary-btn" onClick={handleGenerateSummary} disabled={summarizing}>
                    {summarizing ? 'generating...' : 'generate summary'}
                </button>
                {sentTo && <span className="email-sent-msg">email sent to {sentTo}!</span>}
            </div>
        </div>
    )
}
