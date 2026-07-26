import { useState } from 'react'
import { api } from '../api'

export default function OptionalEnrichment({ farmerId, onDone }) {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const addHistory = async () => {
    setSubmitting(true)
    setError('')
    try {
      await api.recordConsent(farmerId, 'cooperative', true)
      await api.refreshConnector(farmerId, 'cooperative')
      onDone(true)
    } catch {
      setError('Something went wrong. You can add this later.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h1>Raise your limit (optional)</h1>
      <p className="body-text">
        Add your co-op or buyer delivery history to raise your limit. You can skip this and add it
        later -- it never affects whether you qualify.
      </p>
      {error && <p className="error-text">{error}</p>}
      <div className="button-row">
        <button className="btn-secondary" onClick={() => onDone(false)} disabled={submitting}>
          Skip for now
        </button>
        <button className="btn-primary" onClick={addHistory} disabled={submitting}>
          {submitting ? 'Adding...' : 'Add my co-op history'}
        </button>
      </div>
    </div>
  )
}
