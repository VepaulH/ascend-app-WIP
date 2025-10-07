
import React, { useState } from 'react'

export default function Chat({ onSubmitText }) {
  const [text, setText] = useState('I felt good today, meditated 10 minutes')
  const [last, setLast] = useState(null)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState(null)

  const send = async (e) => {
    e.preventDefault()
    setLoading(true); setErr(null)
    try {
      const data = await onSubmitText(text)
      setLast(data)
    } catch (e) {
      setErr('Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <form onSubmit={send} style={{ display: 'flex', gap: 8 }}>
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Free-form text..."
          style={{ flex: 1, padding: 10, borderRadius: 8, border: '1px solid #ccc' }}
        />
        <button disabled={loading} style={{ padding: '10px 14px', borderRadius: 8 }}>
          {loading ? 'Parsing...' : 'Log'}
        </button>
      </form>
      {err && <p style={{ color: 'crimson' }}>{err}</p>}
      {last && (
        <div style={{ marginTop: 12, background: '#f7f7f7', padding: 12, borderRadius: 8 }}>
          <b>Parsed:</b>
          <pre style={{ margin: 0 }}>{JSON.stringify(last, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
