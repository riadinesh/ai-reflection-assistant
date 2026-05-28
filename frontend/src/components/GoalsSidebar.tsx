import { goalActions } from '../hooks/GoalActions'

export default function GoalsSidebar() {
    const { goals, handleEditGoal, handleKeyPress, handleEditDescription, handleDescriptionKeyPress, handleAddGoal, handleDeleteGoal } = goalActions()

    return (
        <div className="sidebar">
            <div className="goals-header">
                <h3>My Goals</h3>
            </div>
            <div className="goals-list">
                <ul>
                    {goals.map(goal => (
                        <li key={goal.id} className="goal-item">
                            <button className="delete-goal-btn" onClick={() => handleDeleteGoal(goal.id)}>✕</button>
                            <div className="goal-content">
                                <textarea
                                    className="goal-title-input"
                                    value={goal.title}
                                    placeholder="Goal title..."
                                    onChange={(e) => handleEditGoal(goal.id, e)}
                                    onKeyDown={(e) => handleKeyPress(goal.id, e)}
                                />
                                <textarea
                                    className="goal-description-input"
                                    value={goal.description}
                                    placeholder="Add a description..."
                                    onChange={(e) => handleEditDescription(goal.id, e)}
                                    onKeyDown={(e) => handleDescriptionKeyPress(goal.id, e)}
                                    onInput={(e) => {
                                        const el = e.target as HTMLTextAreaElement
                                        el.style.height = 'auto'
                                        el.style.height = el.scrollHeight + 'px'
                                    }}
                                />
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="goals-footer">
                <button
                    className="add-goal-btn"
                    onClick={handleAddGoal}
                    disabled={goals.length >= 5}
                >
                    + add goal
                </button>
            </div>
        </div>
    )
}
