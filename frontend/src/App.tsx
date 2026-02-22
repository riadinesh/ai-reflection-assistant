import { useState } from 'react'
import './App.css'
import GoalsSidebar from './components/GoalsSidebar'
import ReflectionPanel from './components/ReflectionPanel'

function App() {

  return (
    <div>
      <GoalsSidebar />
      <ReflectionPanel/>
    </div>
    
  )
}

export default App
