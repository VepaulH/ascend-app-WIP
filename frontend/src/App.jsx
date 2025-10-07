
import React, { useState, useEffect } from 'react'
import Chat from './Chat'
import Dashboard from './Dashboard'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [entries, setEntries] = useState([])

  const refresh = async () => {
    const res = await fetch(`${API_BASE}/api/entries`)
    const data = await res.json()
    setEntries(data)
  }

  useEffect(() => { refresh() }, [])

  const onSubmitText = async (text) => {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })
    const data = await res.json()
    await refresh()
    return data
  }

  return (
    <div style={{ maxWidth: 900, margin: '40px auto', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <h1>Bravura - Ascend</h1>
      <p>Type how your day went. We'll parse, save, and chart it.</p>
      <Chat onSubmitText={onSubmitText} />
      <hr style={{ margin: '24px 0' }} />
      <Dashboard entries={entries} />
    </div>
  )
}
