import { useState } from 'react'
import { api } from '../api'

const PARAMETER_LABELS = {
  cash_flow_stability: 'Cash-Flow Stability',
  repayment_history: 'Repayment History',
  market_linkage: 'Market Linkage',
  social_collateral: 'Social Collateral',
}

const IMPROVEMENT_TIPS = {
  cash_flow_stability:
    'Depositing income through M-Pesa consistently each month would strengthen this.',
  repayment_history: 'Building a track record of on-time payments would raise this over time.',
  market_linkage: 'Consistent deliveries to your co-op or buyer next season would raise this band.',
  social_collateral: 'Longer, continuous membership in a cooperative would raise this band.',
}

const COVERAGE_GATES = new Set(['unfinanced_value_chain', 'out_of_service_area'])

function lowestBandEntry(bands) {
  return Object.entries(bands).sort((a, b) => a[1].points - b[1].points)[0]
}

function money(kes) {
  return `KES ${Number(kes).toLocaleString()}`
}

export default function Completion({ farmerId, name, score, coopAdded, onRestart }) {
  const [current, setCurrent] = useState(score)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const addCoopNow = async () => {
    setSubmitting(true)
    setError('')
    try {
      await api.recordConsent(farmerId, 'cooperative', true)
      await api.refreshConnector(farmerId, 'cooperative')
      const updated = await api.score(farmerId)
      setCurrent(updated)
    } catch {
      setError('Something went wrong updating your offer. Please try again shortly.')
    } finally {
      setSubmitting(false)
    }
  }

  const greeting = name ? `${name}, here` : "Here"

  if (!current.eligible) {
    const coverageIssue = current.gate_failures.some((g) => COVERAGE_GATES.has(g.gate))
    return (
      <div className="card">
        <h1>We can't offer a loan right now</h1>
        <ul className="reasons-list">
          {current.gate_failures.map((g) => (
            <li key={g.gate}>{g.reason}</li>
          ))}
        </ul>
        {coverageIssue && (
          <p className="muted">
            This reflects where we currently operate, not a judgement on you or your farm.
          </p>
        )}
        <button className="btn-secondary" onClick={onRestart}>
          Start over
        </button>
      </div>
    )
  }

  const [lowestParam, lowestBand] = lowestBandEntry(current.parameter_bands)

  return (
    <div className="card">
      <h1>{greeting}'s your result</h1>
      <div className="tier-badge">{current.tier}</div>
      <p className="body-text">
        Your creditworthiness band is <strong>{current.tier}</strong>.
      </p>

      <div className="bands-grid">
        {Object.entries(current.parameter_bands).map(([key, band]) => (
          <div className="band-item" key={key}>
            <p className="band-label">{PARAMETER_LABELS[key]}</p>
            <p className="band-value">{band.label}</p>
            <p className="field-hint">{band.why}</p>
          </div>
        ))}
      </div>

      <div className="offer-box">
        <h2>Your loan offer</h2>
        <p className="offer-amount">{money(current.loan_structuring.max_loan_amount_kes)}</p>
        <p className="body-text">
          {current.loan_structuring.term_months}-month term
          {current.loan_structuring.insurance_mandatory ? ', with required crop insurance' : ''}.
        </p>
      </div>

      <div className="lever-box">
        <p className="toggle-title">One thing that would raise your score</p>
        <p className="field-hint">
          {IMPROVEMENT_TIPS[lowestParam]} (currently {lowestBand.label})
        </p>
      </div>

      {!coopAdded && (
        <div className="lever-box">
          <p className="toggle-title">Have a co-op or buyer history?</p>
          <p className="field-hint">Add it now to see if it raises your limit.</p>
          {error && <p className="error-text">{error}</p>}
          <button className="btn-secondary" onClick={addCoopNow} disabled={submitting}>
            {submitting ? 'Checking...' : 'Add co-op history'}
          </button>
        </div>
      )}

      <button className="btn-secondary" onClick={onRestart}>
        Start a new application
      </button>
    </div>
  )
}
