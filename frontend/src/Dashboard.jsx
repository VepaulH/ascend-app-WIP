
import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'

const moodScale = (mood) => {
  if (!mood) return null
  const map = { sad: 1, stressed: 2, anxious: 2, okay: 3, neutral: 3, good: 4, happy: 5, excited: 5 }
  return map[mood?.toLowerCase?.()] ?? null
}

export default function Dashboard({ entries }) {
  const data = [...entries].reverse().map(e => ({
    ts: new Date(e.timestamp).toLocaleString(),
    mood: e.mood,
    moodScore: moodScale(e.mood),
    duration: e.duration || 0,
    habit: e.habit
  }))

  return (
    <div>
      <h2>Dashboard</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16 }}>
        <div style={{ background: '#f7f7f7', padding: 12, borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Mood over time</h3>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="ts" hide />
                <YAxis domain={[0, 5]} />
                <Tooltip />
                <Line type="monotone" dataKey="moodScore" dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div style={{ background: '#f7f7f7', padding: 12, borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Recent entries</h3>
          <table width="100%" cellPadding="8">
            <thead>
              <tr style={{ textAlign: 'left' }}>
                <th>Time</th><th>Mood</th><th>Habit</th><th>Duration (min)</th><th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {entries.map(e => (
                <tr key={e.id}>
                  <td>{new Date(e.timestamp).toLocaleString()}</td>
                  <td>{e.mood ?? '-'}</td>
                  <td>{e.habit ?? '-'}</td>
                  <td>{e.duration ?? '-'}</td>
                  <td style={{ maxWidth: 420, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{e.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
