import React, { useState, useEffect } from 'react'
const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

function getWeekStart(): string {
    const today = new Date()
    const day = today.getDay()
    const diff = today.getDate() - day + (day === 0 ? -6 : 1)
    const monday = new Date(today.setDate(diff))
    return monday.toISOString().split('T')[0]
}

type Reflection = { id: number, day: string, content: string }

export function reflectionActions() {
    const weekStart = getWeekStart()
    const [reflectionMap, setReflectionMap] = useState<Record<string, Reflection>>({})

    useEffect(() => {
        fetch(`http://localhost:8000/reflections?week_start=${weekStart}`)
            .then(res => res.json())
            .then(data => {
                const map = Object.fromEntries(data.map((r: Reflection) => [r.day, r]))
                setReflectionMap(map)
            })
    }, [])

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
            console.log(weekStart)
            e.currentTarget.blur()
            fetch("http://localhost:8000/reflections?week_start=" + weekStart, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    week_start: weekStart,
                    day: day,
                    content: e.currentTarget.value
                })
            })
        }
    }

    return { days: DAYS, reflectionMap, handleContentChange, handleKeyPress }
}
