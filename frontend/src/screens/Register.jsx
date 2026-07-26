import { useState } from 'react'
import { api } from '../api'

const TENURE_OPTIONS = [
  { value: 'owner_occupier_titled', label: 'I own it, with title deed' },
  { value: 'owner_occupier_no_title', label: 'I own it, no title deed yet' },
  { value: 'family_land_no_title', label: 'Family land' },
  { value: 'leasehold_informal', label: 'Leased / rented' },
  { value: 'communal', label: 'Communal land' },
]

export default function Register({ prequalifyData, onRegistered }) {
  const [name, setName] = useState('')
  const [nationalId, setNationalId] = useState('')
  const [tenureStatus, setTenureStatus] = useState('')
  const [secondaryCrops, setSecondaryCrops] = useState('')
  const [landSizeAcres, setLandSizeAcres] = useState('')
  const [gps, setGps] = useState(null)
  const [gpsError, setGpsError] = useState('')
  const [useManualGps, setUseManualGps] = useState(false)
  const [locating, setLocating] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const captureLocation = () => {
    setGpsError('')
    if (!navigator.geolocation) {
      setGpsError('Location is not available on this device. Enter it manually below.')
      setUseManualGps(true)
      return
    }
    setLocating(true)
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setGps({ lat: pos.coords.latitude, lon: pos.coords.longitude })
        setLocating(false)
      },
      () => {
        setGpsError('Could not get your location. Enter it manually below.')
        setUseManualGps(true)
        setLocating(false)
      },
      { timeout: 8000 },
    )
  }

  const submit = async (e) => {
    e.preventDefault()
    if (!gps) {
      setGpsError('A GPS pin is required to continue.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      const { farmer_id } = await api.createFarmer({
        phone: prequalifyData.phone,
        national_id: nationalId,
        gps_pin: gps,
        tenure_status: tenureStatus,
        crop: prequalifyData.crop,
        secondary_crops: secondaryCrops
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean),
        land_size_acres: Number(landSizeAcres),
        county: prequalifyData.county,
        ward: prequalifyData.ward,
        land_size_band: prequalifyData.land_size_band,
        loan_purpose: prequalifyData.loan_purpose,
      })
      onRegistered(farmer_id, { name })
    } catch {
      setError('Something went wrong saving your details. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h1>Tell us about your farm</h1>
      <p className="body-text">You or a field agent can fill this in.</p>
      <form onSubmit={submit} className="form">
        <label>
          Full name
          <input required value={name} onChange={(e) => setName(e.target.value)} />
        </label>

        <label>
          National ID number
          <input required value={nationalId} onChange={(e) => setNationalId(e.target.value)} />
        </label>

        <label>
          How you hold this land
          <select required value={tenureStatus} onChange={(e) => setTenureStatus(e.target.value)}>
            <option value="" disabled>
              Select an option
            </option>
            {TENURE_OPTIONS.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Land size (acres)
          <input
            required
            type="number"
            step="0.1"
            min="0.1"
            value={landSizeAcres}
            onChange={(e) => setLandSizeAcres(e.target.value)}
          />
        </label>

        <label>
          Other crops you grow (optional)
          <input
            placeholder="e.g. maize, beans"
            value={secondaryCrops}
            onChange={(e) => setSecondaryCrops(e.target.value)}
          />
        </label>

        <div className="gps-block">
          <p className="field-hint">
            Pinning your farm's location unlocks a free satellite crop-health check -- no visit
            needed.
          </p>
          <button type="button" className="btn-secondary" onClick={captureLocation}>
            {locating ? 'Finding you...' : gps ? 'Location captured ✓' : 'Use my current location'}
          </button>
          {gps && (
            <p className="muted">
              {gps.lat.toFixed(4)}, {gps.lon.toFixed(4)}
            </p>
          )}
          {useManualGps && (
            <div className="manual-gps">
              {gpsError && <p className="error-text">{gpsError}</p>}
              <label>
                Latitude
                <input
                  type="number"
                  step="any"
                  onChange={(e) => {
                    setGps((g) => ({ lat: Number(e.target.value), lon: g?.lon ?? 0 }))
                    setGpsError('')
                  }}
                />
              </label>
              <label>
                Longitude
                <input
                  type="number"
                  step="any"
                  onChange={(e) => {
                    setGps((g) => ({ lat: g?.lat ?? 0, lon: Number(e.target.value) }))
                    setGpsError('')
                  }}
                />
              </label>
            </div>
          )}
        </div>

        {error && <p className="error-text">{error}</p>}

        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'Saving...' : 'Continue'}
        </button>
      </form>
    </div>
  )
}
