import { useEffect, useState } from 'react'
import { api } from '../api'

const LAND_SIZE_LABELS = {
  under_1_acre: 'Under 1 acre',
  '1_to_2_acres': '1-2 acres',
  '2_to_5_acres': '2-5 acres',
  over_5_acres: 'Over 5 acres',
}

const LOAN_PURPOSES = [
  { value: 'input_finance', label: 'Buy seeds, fertilizer or other inputs' },
  { value: 'equipment', label: 'Buy or lease equipment' },
  { value: 'irrigation', label: 'Irrigation or water access' },
  { value: 'other', label: 'Other farm need' },
]

export default function PreQualify({ onQualified }) {
  const [config, setConfig] = useState(null)
  const [form, setForm] = useState({
    phone: '',
    county: '',
    ward: '',
    crop: '',
    land_size_band: '',
    loan_purpose: 'input_finance',
  })
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.eligibilityConfig().then(setConfig).catch(() => setError('Could not reach the server.'))
  }, [])

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }))

  const submit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const res = await api.prequalify(form)
      setResult(res)
      if (res.prequalified) {
        onQualified(form)
      }
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const reset = () => {
    setResult(null)
    setForm((f) => ({ ...f, crop: '', county: '' }))
  }

  if (result && !result.prequalified) {
    return (
      <div className="card">
        <p className="step-indicator">Step 1 of 2 minutes</p>
        <h1>Not quite a match yet</h1>
        <p className="body-text">
          Based on what you've shared, this isn't something we can offer here right now:
        </p>
        <ul className="reasons-list">
          {result.reasons.map((r) => (
            <li key={r}>{r}</li>
          ))}
        </ul>
        <p className="muted">
          This is a coverage limitation on our end, not a judgement on you or your farm.
        </p>
        <button className="btn-secondary" onClick={reset}>
          Try different details
        </button>
      </div>
    )
  }

  return (
    <div className="card">
      <p className="step-indicator">Step 1 of 2 minutes</p>
      <h1>Check if you qualify</h1>
      <p className="body-text">
        A few quick questions about your farm. No paperwork yet, and this won't affect your
        credit.
      </p>
      <form onSubmit={submit} className="form">
        <label>
          Phone number
          <input
            required
            type="tel"
            placeholder="+254 7XX XXX XXX"
            value={form.phone}
            onChange={update('phone')}
          />
        </label>

        <label>
          County
          <select required value={form.county} onChange={update('county')}>
            <option value="" disabled>
              Select county
            </option>
            {(config?.serviceable_counties ?? []).map((c) => (
              <option key={c} value={c}>
                {c.replace(/_/g, ' ')}
              </option>
            ))}
          </select>
        </label>

        <label>
          Ward
          <input
            required
            type="text"
            placeholder="e.g. Kapsoit"
            value={form.ward}
            onChange={update('ward')}
          />
        </label>

        <label>
          Main crop
          <select required value={form.crop} onChange={update('crop')}>
            <option value="" disabled>
              Select crop
            </option>
            {(config?.financed_value_chains ?? []).map((c) => (
              <option key={c} value={c}>
                {c.replace(/_/g, ' ')}
              </option>
            ))}
          </select>
        </label>

        <label>
          Land size
          <select required value={form.land_size_band} onChange={update('land_size_band')}>
            <option value="" disabled>
              Select land size
            </option>
            {(config?.land_size_bands ?? []).map((b) => (
              <option key={b} value={b}>
                {LAND_SIZE_LABELS[b] ?? b}
              </option>
            ))}
          </select>
        </label>

        <label>
          What's the loan for?
          <select value={form.loan_purpose} onChange={update('loan_purpose')}>
            {LOAN_PURPOSES.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </label>

        {error && <p className="error-text">{error}</p>}

        <button className="btn-primary" type="submit" disabled={submitting || !config}>
          {submitting ? 'Checking...' : 'Check if I qualify'}
        </button>
      </form>
    </div>
  )
}
