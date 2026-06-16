import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

import { LoadingSkeleton } from '../components/LoadingSkeleton'
import { checkEligibility, combineSubsidies } from '../services/api'
import type { CombinationResponse, EligibilityRequest, EligibilityResponse } from '../types/api'

const defaultInput: EligibilityRequest = {
  frs_score: 0,
  current_savings_uf: 0,
  owns_property: false,
  context: 'urban',
}

export function ResultsPage() {
  const location = useLocation()
  const input = useMemo(() => (location.state as EligibilityRequest) ?? defaultInput, [location.state])
  const [data, setData] = useState<EligibilityResponse | null>(null)
  const [combination, setCombination] = useState<CombinationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    checkEligibility(input)
      .then((response) => {
        setData(response)
        const selected = response.ranked_subsidies.filter((item) => item.eligible).slice(0, 2).map((item) => item.subsidy_id)
        if (selected.length > 0) {
          return combineSubsidies(selected).then(setCombination)
        }
      })
      .catch(() => setError('No se pudo cargar la recomendación. Intente nuevamente.'))
  }, [input])

  if (error) {
    return <p className="rounded bg-red-100 p-4 text-red-700">{error}</p>
  }

  if (!data) {
    return <LoadingSkeleton />
  }

  return (
    <section className="space-y-4">
      <div className="rounded-lg bg-white p-4 shadow">
        <h1 className="text-xl font-semibold text-minvuBlue">Resultado de elegibilidad</h1>
        <p>Mejor opción: <strong>{data.best_match_subsidy_id ?? 'Sin coincidencias elegibles por ahora'}</strong></p>
      </div>

      <div className="grid gap-3">
        {data.ranked_subsidies.map((item) => (
          <article key={item.subsidy_id} className="rounded-lg bg-white p-4 shadow">
            <h2 className="font-semibold">{item.subsidy_name}</h2>
            <p>Estado: {item.eligible ? 'Elegible' : 'No elegible aún'}</p>
            <p>Beneficio: {item.benefit_uf} UF</p>
            <p>Plazo estimado: {item.estimated_timeline_months} meses</p>
            {item.requirement_gaps.length > 0 && (
              <ul className="mt-2 list-disc pl-5 text-sm text-amber-700">
                {item.requirement_gaps.map((gap) => (
                  <li key={gap}>{gap}</li>
                ))}
              </ul>
            )}
            <Link className="mt-2 inline-block text-minvuBlue underline" to={`/subsidy/${item.subsidy_id}`}>
              Ver detalle del subsidio
            </Link>
          </article>
        ))}
      </div>

      {combination && (
        <div className="rounded-lg bg-minvuLight p-4">
          <h2 className="font-semibold text-minvuBlue">Paquete combinado sugerido</h2>
          <p>Total potencial: {combination.total_package_uf} UF</p>
          {combination.warnings.map((warning) => (
            <p key={warning} className="text-sm text-amber-700">{warning}</p>
          ))}
        </div>
      )}

      <Link className="inline-flex rounded bg-minvuBlue px-4 py-2 text-white" to="/projects">Buscar proyectos compatibles</Link>
    </section>
  )
}
