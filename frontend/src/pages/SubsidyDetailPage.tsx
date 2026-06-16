import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { listSubsidies } from '../services/api'
import type { Subsidy } from '../types/api'

export function SubsidyDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [subsidy, setSubsidy] = useState<Subsidy | null>(null)

  useEffect(() => {
    listSubsidies().then((items) => setSubsidy(items.find((item) => item.id === id) ?? null))
  }, [id])

  if (!subsidy) {
    return <p className="rounded bg-white p-4 shadow">No se encontró información para este subsidio.</p>
  }

  return (
    <article className="space-y-2 rounded bg-white p-6 shadow">
      <h1 className="text-2xl font-semibold text-minvuBlue">{subsidy.name}</h1>
      <p>Decreto: {subsidy.decree}</p>
      <p>Rango FRS: {subsidy.frs_min} - {subsidy.frs_max}</p>
      <p>Beneficio máximo: {subsidy.benefit_uf} UF</p>
      <p>Ahorro mínimo: {subsidy.required_savings_uf} UF</p>
      <p>Modalidad: {subsidy.modality}</p>
      <p>Períodos habituales: {subsidy.postulation_periods.join(', ')}</p>
      <p>Combinable con: {subsidy.compatible_with.join(', ')}</p>
      <p className="rounded bg-minvuLight p-3">FAQ: verifica siempre documentación y llamados activos en SERVIU para confirmar requisitos vigentes.</p>
    </article>
  )
}
