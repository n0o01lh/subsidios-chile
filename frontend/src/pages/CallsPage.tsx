import { useEffect, useState } from 'react'

import { listCalls } from '../services/api'
import type { PostulationCall } from '../types/api'

export function CallsPage() {
  const [calls, setCalls] = useState<PostulationCall[]>([])

  useEffect(() => {
    listCalls().then(setCalls)
  }, [])

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-minvuBlue">Llamados activos a postulación</h1>
      {calls.map((call) => (
        <article key={call.id} className="rounded bg-white p-4 shadow">
          <h2 className="font-semibold">{call.subsidy_program}</h2>
          <p>Región: {call.region}</p>
          <p>Apertura: {call.opening_date}</p>
          <p>Cierre: {call.closing_date}</p>
          <p>Cupos: {call.available_quotas}</p>
          <p>{call.requirements}</p>
          <a className="text-minvuBlue underline" href={call.source_url} target="_blank" rel="noreferrer">Ver fuente SERVIU</a>
        </article>
      ))}
    </section>
  )
}
