import { useState } from 'react'
import { api } from '../api'

export default function ConsentFinancial({ farmerId, onDone }) {
  const [mpesaConsent, setMpesaConsent] = useState(false)
  const [existingLoan, setExistingLoan] = useState(false)
  const [offFarmIncome, setOffFarmIncome] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      if (mpesaConsent) {
        await api.recordConsent(farmerId, 'mpesa', true)
        await api.refreshConnector(farmerId, 'agrovet_mpesa')
      }
      onDone()
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h1>Help us see your cash flow</h1>
      <p className="body-text">Each of these is optional, and unlocks a better rate on its own.</p>
      <form onSubmit={submit} className="form">
        <div className="toggle-row">
          <div>
            <p className="toggle-title">Share my M-Pesa statement</p>
            <p className="field-hint">
              Lets us see regular income even without a bank account -- unlocks a better rate.
            </p>
          </div>
          <input
            type="checkbox"
            checked={mpesaConsent}
            onChange={(e) => setMpesaConsent(e.target.checked)}
          />
        </div>

        <div className="toggle-row">
          <div>
            <p className="toggle-title">I currently have another loan</p>
            <p className="field-hint">Helps us size a loan you can comfortably repay.</p>
          </div>
          <input
            type="checkbox"
            checked={existingLoan}
            onChange={(e) => setExistingLoan(e.target.checked)}
          />
        </div>

        <div className="toggle-row">
          <div>
            <p className="toggle-title">I have income outside my farm</p>
            <p className="field-hint">Off-farm income can strengthen your application.</p>
          </div>
          <input
            type="checkbox"
            checked={offFarmIncome}
            onChange={(e) => setOffFarmIncome(e.target.checked)}
          />
        </div>

        {error && <p className="error-text">{error}</p>}

        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'Saving...' : 'Continue'}
        </button>
      </form>
    </div>
  )
}
