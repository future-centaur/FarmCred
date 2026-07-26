import { useState } from 'react'
import { api } from '../api'

export default function CRBNotice({ farmerId, onScored }) {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const proceed = async () => {
    setSubmitting(true)
    setError('')
    try {
      await api.recordConsent(farmerId, 'crb', true)
      await api.refreshConnector(farmerId, 'crb_paygo')
      const result = await api.score(farmerId)
      onScored(result)
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h1>One last check</h1>
      <p className="body-text">
        Before we give you a final decision, we're going to run a credit bureau check. This looks
        at any existing loans or repayment history to make sure any loan we offer is one you can
        manage on top of what you already owe.
      </p>
      <p className="muted">This is a standard check and will not affect your score on its own.</p>
      {error && <p className="error-text">{error}</p>}
      <button className="btn-primary" onClick={proceed} disabled={submitting}>
        {submitting ? 'Checking...' : 'I understand, continue'}
      </button>
    </div>
  )
}
