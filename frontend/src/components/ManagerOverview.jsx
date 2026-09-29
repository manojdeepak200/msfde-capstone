function ClaimLinks({ ids, onSelectClaim }) {
  if (!ids?.length) return <span className="muted">None</span>
  return (
    <span className="claim-links">
      {ids.map((claimId) => (
        <button key={claimId} className="claim-link" onClick={() => onSelectClaim(claimId)}>
          {claimId}
        </button>
      ))}
    </span>
  )
}

function InsightList({ title, rows, labelKey, onSelectClaim, emptyText = 'No signals in this claim set.' }) {
  return (
    <section className="manager-insight">
      <h2>{title}</h2>
      {!rows?.length && <p className="muted">{emptyText}</p>}
      {rows?.map((row) => (
        <div className="insight-row" key={row[labelKey]}>
          <div>
            <strong>{row[labelKey].replaceAll('_', ' ')}</strong>
            <span className="muted">{row.count} claim{row.count === 1 ? '' : 's'}</span>
          </div>
          <ClaimLinks ids={row.claim_ids} onSelectClaim={onSelectClaim} />
        </div>
      ))}
    </section>
  )
}

function Metric({ label, value, claimIds, onSelectClaim }) {
  return (
    <div className="stat">
      <span className="label">{label}</span>
      <strong>{value}</strong>
      <details className="metric-trace">
        <summary>View {claimIds.length} claim{claimIds.length === 1 ? '' : 's'}</summary>
        <ClaimLinks ids={claimIds} onSelectClaim={onSelectClaim} />
      </details>
    </div>
  )
}

export default function ManagerOverview({ overview, onSelectClaim }) {
  const recommendations = overview.recommendation_mix || {}

  return (
    <section className="manager-dashboard" aria-label="Claims operations overview">
      <div className="overview">
        <Metric label="Processed" value={overview.total_claims} claimIds={overview.processed_claim_ids} onSelectClaim={onSelectClaim} />
        <Metric label="Request info recommendation" value={overview.request_information_claim_ids.length} claimIds={overview.request_information_claim_ids} onSelectClaim={onSelectClaim} />
        <Metric label="Refer recommendation" value={overview.refer_recommendation_claim_ids.length} claimIds={overview.refer_recommendation_claim_ids} onSelectClaim={onSelectClaim} />
        <Metric label="No findings" value={`${Math.round(overview.no_finding_rate * 100)}%`} claimIds={overview.no_finding_claim_ids} onSelectClaim={onSelectClaim} />
        <Metric label="Avg. preparation" value={`${overview.average_elapsed_seconds}s`} claimIds={overview.processed_claim_ids} onSelectClaim={onSelectClaim} />
      </div>

      <div className="manager-insights">
        <InsightList title="Most common findings" rows={overview.top_findings} labelKey="code" onSelectClaim={onSelectClaim} />
        <InsightList title="Missing evidence" rows={overview.missing_documents} labelKey="document" onSelectClaim={onSelectClaim} />
        <InsightList title="Estimate distribution" rows={overview.estimate_buckets} labelKey="band" onSelectClaim={onSelectClaim} />
      </div>

      <section className="manager-insight pattern-insights">
        <div className="row">
          <h2>Cross-claim patterns</h2>
          <span className="muted">Indicators only; not fraud findings</span>
        </div>
        {!overview.cross_claim_patterns.length && <p className="muted">No cross-claim patterns detected in the processed set.</p>}
        {overview.cross_claim_patterns.map((pattern) => (
          <div className="pattern-row" key={`${pattern.code}-${pattern.shared_value}`}>
            <strong>{pattern.shared_value}</strong>
            <span>{pattern.message}</span>
            <span className="muted">Claims: {pattern.claim_ids.join(', ')}</span>
            <span className="muted">History source: <ClaimLinks ids={pattern.source_claim_ids} onSelectClaim={onSelectClaim} /></span>
          </div>
        ))}
        <p className="muted governance-note">Book-level comparisons use fictional training data. Production access must be scoped to an authorised claims cohort.</p>
      </section>

      <div className="queue-trace">
        <span className="recommendation-trace">
          Recommendation mix:
          {Object.entries(recommendations).map(([recommendation, count]) => (
            <span key={recommendation}>{recommendation.replaceAll('_', ' ')} {count} <ClaimLinks ids={overview.recommendation_claim_ids[recommendation]} onSelectClaim={onSelectClaim} /></span>
          ))}
        </span>
        <span>Verification queue ({overview.awaiting_verification} claim{overview.awaiting_verification === 1 ? '' : 's'}): <ClaimLinks ids={overview.verification_claim_ids} onSelectClaim={onSelectClaim} /></span>
      </div>
    </section>
  )
}