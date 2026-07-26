import { useState } from 'react'
import './App.css'
import PreQualify from './screens/PreQualify'
import Register from './screens/Register'
import ConsentFinancial from './screens/ConsentFinancial'
import BackgroundEnrichment from './screens/BackgroundEnrichment'
import OptionalEnrichment from './screens/OptionalEnrichment'
import CRBNotice from './screens/CRBNotice'
import Completion from './screens/Completion'

const PHASES = {
  PREQUALIFY: 'prequalify',
  REGISTER: 'register',
  CONSENT_FINANCIAL: 'consent_financial',
  BACKGROUND: 'background',
  OPTIONAL: 'optional',
  CRB: 'crb',
  COMPLETION: 'completion',
}

const initialState = {
  phase: PHASES.PREQUALIFY,
  prequalifyData: null,
  farmerId: null,
  name: '',
  coopAdded: false,
  score: null,
}

export default function App() {
  const [state, setState] = useState(initialState)

  const restart = () => setState(initialState)

  return (
    <div className="app-shell">
      <header className="brand">FarmCred</header>
      <main>
        {state.phase === PHASES.PREQUALIFY && (
          <PreQualify
            onQualified={(prequalifyData) =>
              setState((s) => ({ ...s, phase: PHASES.REGISTER, prequalifyData }))
            }
          />
        )}

        {state.phase === PHASES.REGISTER && (
          <Register
            prequalifyData={state.prequalifyData}
            onRegistered={(farmerId, { name }) =>
              setState((s) => ({ ...s, phase: PHASES.CONSENT_FINANCIAL, farmerId, name }))
            }
          />
        )}

        {state.phase === PHASES.CONSENT_FINANCIAL && (
          <ConsentFinancial
            farmerId={state.farmerId}
            onDone={() => setState((s) => ({ ...s, phase: PHASES.BACKGROUND }))}
          />
        )}

        {state.phase === PHASES.BACKGROUND && (
          <BackgroundEnrichment onDone={() => setState((s) => ({ ...s, phase: PHASES.OPTIONAL }))} />
        )}

        {state.phase === PHASES.OPTIONAL && (
          <OptionalEnrichment
            farmerId={state.farmerId}
            onDone={(coopAdded) => setState((s) => ({ ...s, phase: PHASES.CRB, coopAdded }))}
          />
        )}

        {state.phase === PHASES.CRB && (
          <CRBNotice
            farmerId={state.farmerId}
            onScored={(score) => setState((s) => ({ ...s, phase: PHASES.COMPLETION, score }))}
          />
        )}

        {state.phase === PHASES.COMPLETION && (
          <Completion
            farmerId={state.farmerId}
            name={state.name}
            score={state.score}
            coopAdded={state.coopAdded}
            onRestart={restart}
          />
        )}
      </main>
    </div>
  )
}
