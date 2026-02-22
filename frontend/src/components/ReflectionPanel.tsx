import { reflectionActions } from '../hooks/ReflectionActions'

export default function ReflectionPanel() {
    const { days, reflectionMap, handleContentChange, handleKeyPress } = reflectionActions()

    return (
        <div className="reflection-panel">
            <h3 className="reflection-header">This Week's Reflections</h3>
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
