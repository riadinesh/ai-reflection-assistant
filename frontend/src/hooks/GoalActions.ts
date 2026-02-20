import React, { useState, useEffect } from 'react'

// Function imported into GoalsSidebar.tsx
export function goalActions() {
    const [goals, setGoals] = useState<{id: number, title: string, description: string}[]>([])

    // On first render, load goals
    useEffect(() => {
        fetch("http://localhost:8000/goals")
            .then(res => res.json())
            .then(data => setGoals(data))
    }, [])

    // Edit goal
    const handleEditGoal = (id: number, e: React.ChangeEvent<HTMLInputElement>) => {
        setGoals(goals.map(g => g.id === id ? { ...g, title: e.target.value } : g))
    }

    // Update goal on database
    const handleKeyPress = (id: number, e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            e.currentTarget.blur()
            fetch("http://localhost:8000/goals/" + id, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: e.currentTarget.value })
            })
        }
    }

    return { goals, handleEditGoal, handleKeyPress }
}
