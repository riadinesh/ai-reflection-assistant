import { goalActions } from '../hooks/GoalActions'

export default function GoalsSidebar() {
    const { goals, handleEditGoal, handleKeyPress } = goalActions()

    return (
        <div className="sidebar">
            <div className="goals-header">
                <h3>My Goals</h3>
            </div>
            <div className="goals-list">
                <ul>
                    {goals.map(goal => (
                        <li key={goal.id} className="goal-item">
                            <input
                                type="text"
                                value={goal.title}
                                onChange={(e) => handleEditGoal(goal.id, e)}
                                onKeyDown={(e) => handleKeyPress(goal.id, e)}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}
