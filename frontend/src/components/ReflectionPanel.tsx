import { reflectionActions } from '../hooks/ReflectionActions'

export default function ReflectionPanel() {
    const { days, reflectionMap, dateRangeLabel, handleContentChange, handleKeyPress, goToPreviousWeek, goToNextWeek, isCurrentWeek } = reflectionActions()

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
                            placeholder="Write your reflection..."
                            value={reflectionMap[day]?.content ?? ""}
                            onChange={(e) => handleContentChange(day, e)}
                            onKeyDown={(e) => handleKeyPress(day, e)}
                        />
                    </li>
                ))}
            </ul>
        </div>
    )
}
