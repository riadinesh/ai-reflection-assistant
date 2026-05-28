import React, { useState, useEffect } from 'react'

// Function imported into GoalsSidebar.tsx
export function goalActions() {
    const [goals, setGoals] = useState<{id: number, title: string, description: string}[]>([])

    const token = localStorage.getItem('token')
    const authHeaders = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }

    // On first render, load goals
    useEffect(() => {
        fetch("http://localhost:8000/goals", { headers: authHeaders })
            .then(res => res.json())
            .then(data => setGoals(data))
    }, [])

    // Edit goal title
    const handleEditGoal = (id: number, e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setGoals(goals.map(g => g.id === id ? { ...g, title: e.target.value } : g))
    }

    // Update goal title on database
    const handleKeyPress = (id: number, e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            e.currentTarget.blur()
            const goal = goals.find(g => g.id === id)
            if (!goal) return
            fetch("http://localhost:8000/goals/" + id, {
                method: "PUT",
                headers: authHeaders,
                body: JSON.stringify({ title: goal.title, description: goal.description })
            })
        }
    }

    // Edit goal description in local state
    const handleEditDescription = (id: number, e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setGoals(goals.map(g => g.id === id ? { ...g, description: e.target.value } : g))
    }

    // Save description to database on Enter
    const handleDescriptionKeyPress = (id: number, e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            e.currentTarget.blur()
            const goal = goals.find(g => g.id === id)
            if (!goal) return
            fetch("http://localhost:8000/goals/" + id, {
                method: "PUT",
                headers: authHeaders,
                body: JSON.stringify({ title: goal.title, description: goal.description })
            })
        }
    }

    // Delete a goal
    const handleDeleteGoal = (id: number) => {
        fetch("http://localhost:8000/goals/" + id, { method: "DELETE", headers: authHeaders })
            .then(() => setGoals(goals.filter(g => g.id !== id)))
    }

    // Add a new blank goal
    const handleAddGoal = () => {
        fetch("http://localhost:8000/goals", {
            method: "POST",
            headers: authHeaders,
            body: JSON.stringify({ title: "", description: "" })
        })
            .then(res => res.json())
            .then(data => setGoals([...goals, data]))
    }

    return { goals, handleEditGoal, handleKeyPress, handleEditDescription, handleDescriptionKeyPress, handleAddGoal, handleDeleteGoal }
}
