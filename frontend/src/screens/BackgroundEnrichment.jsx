import { useEffect } from 'react'

export default function BackgroundEnrichment({ onDone }) {
  useEffect(() => {
    const t = setTimeout(onDone, 1600)
    return () => clearTimeout(t)
  }, [onDone])

  return (
    <div className="card center">
      <div className="spinner" />
      <p className="body-text">Verifying your farm details...</p>
      <p className="muted">Checking your land registry and satellite crop-health records.</p>
    </div>
  )
}
