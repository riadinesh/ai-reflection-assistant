import React, { useState, useEffect } from 'react'

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
function getMondayOfWeek(offset: number = 0): Date {
    const today = new Date()
    const day = today.getDay()
    const diff = today.getDate() - day + (day === 0 ? -6 : 1) + (offset * 7)
    return new Date(today.getFullYear(), today.getMonth(), diff)
}

function formatISODate(date: Date): string {
    return date.toISOString().split('T')[0]
}

function formatLabel(date: Date): string {
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })
}


type Reflection = { id: number, day: string, content: string }

export function reflectionActions() {
    const token = localStorage.getItem('token')
    const authHeaders = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }

    const [weekOffset, setWeekOffset] = useState(0)
    const monday = getMondayOfWeek(weekOffset)
    const sunday = new Date(monday)
    sunday.setDate(sunday.getDate() + 6)

    const weekStart = formatISODate(monday)
    const dateRangeLabel = `${formatLabel(monday)} - ${formatLabel(sunday)}`

    const [reflectionMap, setReflectionMap] = useState<Record<string, Reflection>>({})

    // Navigation to previous/next week
    // When offset changes (state changes), page re-renders and useEffect runs with a new weekStart
    const goToPreviousWeek = () => setWeekOffset(prev => prev - 1)
    const goToNextWeek = () => setWeekOffset(prev => prev + 1)
    const isCurrentWeek = weekOffset === 0 // If on current week, disable next week button

    useEffect(() => {
        fetch(`http://localhost:8000/reflections?week_start=${weekStart}`, { headers: authHeaders })
            .then(res => res.json())
            .then(data => {
                const map = Object.fromEntries(data.map((r: Reflection) => [r.day, r]))
                setReflectionMap(map)
            })
    }, [weekStart])

    const handleContentChange = (day: string, e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setReflectionMap(prev => ({
            ...prev,
            [day]: { ...prev[day], content: e.target.value }
        }))
        // auto grows the text box
        e.target.style.height = 'auto'
        e.target.style.height = `${e.target.scrollHeight}px`
    }

    const handleKeyPress = (day: string, e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter') {
            e.currentTarget.blur()
            fetch("http://localhost:8000/reflections", {
                method: "POST",
                headers: authHeaders,
                body: JSON.stringify({
                    week_start: weekStart,
                    day: day,
                    content: e.currentTarget.value
                })
            })
        }
    }

    return { days: DAYS, reflectionMap, dateRangeLabel, handleContentChange, handleKeyPress, goToPreviousWeek, goToNextWeek, isCurrentWeek }
}
