const BASE = '/v1'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || detail
    } catch {
      // ignore
    }
    throw new Error(detail)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  prequalify: (body) => request('/prequalify', { method: 'POST', body: JSON.stringify(body) }),

  eligibilityConfig: () => request('/config/eligibility'),

  createFarmer: (body) => request('/farmers', { method: 'POST', body: JSON.stringify(body) }),

  getFarmer: (farmerId) => request(`/farmers/${farmerId}`),

  recordConsent: (farmerId, category, granted, locale = 'en') =>
    request(`/farmers/${farmerId}/consent`, {
      method: 'POST',
      body: JSON.stringify({ category, granted, locale }),
    }),

  refreshConnector: (farmerId, source) =>
    request(`/farmers/${farmerId}/connectors/${source}/refresh`, { method: 'POST' }),

  score: (farmerId) => request(`/farmers/${farmerId}/score`, { method: 'POST' }),

  latestScore: (farmerId) => request(`/farmers/${farmerId}/score`),

  scoreHistory: (farmerId) => request(`/farmers/${farmerId}/score/history`),
}
