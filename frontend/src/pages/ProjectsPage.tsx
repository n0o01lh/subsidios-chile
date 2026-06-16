import { useState } from 'react'
import type { FormEvent } from 'react'

import { useLocationData } from '../hooks/useLocationData'
import { listProjects } from '../services/api'
import type { Project } from '../types/api'

export function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([])
  const [region, setRegion] = useState('13')
  const [commune, setCommune] = useState('')
  const { regions, communesByRegionId, loading: locationLoading } = useLocationData()

  const communes = communesByRegionId[Number(region)] ?? []

  const handleRegionChange = (newRegion: string) => {
    setRegion(newRegion)
    setCommune('')
  }

  const load = async (search = new URLSearchParams()) => {
    const data = await listProjects(search)
    setProjects(data)
  }

  const onSubmit = (event: FormEvent) => {
    event.preventDefault()
    const params = new URLSearchParams()
    if (region) params.set('region', region)
    if (commune) params.set('commune', commune)
    load(params).catch(() => setProjects([]))
  }

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-minvuBlue">Proyectos disponibles</h1>
      <form className="grid gap-3 rounded bg-white p-4 shadow md:grid-cols-3" onSubmit={onSubmit}>
        <label className="flex flex-col gap-1">
          Región
          <select
            className="rounded border p-2"
            value={region}
            onChange={(event) => handleRegionChange(event.target.value)}
            disabled={locationLoading}
          >
            {locationLoading && <option value="">Cargando regiones…</option>}
            {regions.map((r) => (
              <option key={r.id} value={String(r.id)}>
                {r.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1">
          Comuna
          <select
            className="rounded border p-2"
            value={commune}
            onChange={(event) => setCommune(event.target.value)}
            disabled={locationLoading || communes.length === 0}
          >
            <option value="">Todas las comunas</option>
            {communes.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        <button className="self-end rounded bg-minvuBlue px-4 py-2 text-white" disabled={locationLoading}>
          Filtrar
        </button>
      </form>

      <div className="grid gap-3 md:grid-cols-2">
        {projects.map((project) => (
          <article key={project.id} className="rounded-lg bg-white p-4 shadow">
            <h2 className="font-semibold">{project.name}</h2>
            <p>{project.commune} - Región {project.region}</p>
            <p>Programa compatible: {project.subsidy_program}</p>
            <p>Precio: {project.min_price_uf} - {project.max_price_uf} UF</p>
            <p>Unidades: {project.available_units}</p>
            <a className="text-minvuBlue underline" href={project.source_url} target="_blank" rel="noreferrer">Ir a fuente oficial</a>
          </article>
        ))}
      </div>
    </section>
  )
}
