import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'

import type { EligibilityRequest } from '../types/api'

export function HomePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState<EligibilityRequest>({
    frs_score: 0,
    monthly_household_income: undefined,
    family_members: undefined,
    current_savings_uf: 0,
    region: undefined,
    owns_property: false,
    age: undefined,
    context: 'urban',
  })

  const onSubmit = (event: FormEvent) => {
    event.preventDefault()
    navigate('/results', { state: form })
  }

  return (
    <section className="space-y-4 rounded-lg bg-white p-6 shadow">
      <h1 className="text-2xl font-semibold text-minvuBlue">Encuentra tu mejor subsidio habitacional</h1>
      <p>Ingresa tu puntaje FRS y tu situación actual para obtener recomendaciones personalizadas.</p>
      <form className="grid gap-4 md:grid-cols-2" onSubmit={onSubmit}>
        <label className="flex flex-col gap-1">
          Puntaje FRS
          <input aria-label="Puntaje FRS" className="rounded border p-2" type="number" min={0} max={100000} required value={form.frs_score} onChange={(event) => setForm((prev) => ({ ...prev, frs_score: Number(event.target.value) }))} />
        </label>
        <label className="flex flex-col gap-1">
          Ingreso mensual hogar (CLP)
          <input aria-label="Ingreso mensual" className="rounded border p-2" type="number" min={0} value={form.monthly_household_income ?? ''} onChange={(event) => setForm((prev) => ({ ...prev, monthly_household_income: event.target.value ? Number(event.target.value) : undefined }))} />
        </label>
        <label className="flex flex-col gap-1">
          Ahorro en libreta MINVU (UF)
          <input aria-label="Ahorro en UF" className="rounded border p-2" type="number" min={0} value={form.current_savings_uf ?? 0} onChange={(event) => setForm((prev) => ({ ...prev, current_savings_uf: Number(event.target.value) }))} />
        </label>
        <label className="flex flex-col gap-1">
          Región (1-16)
          <input aria-label="Región" className="rounded border p-2" type="number" min={1} max={16} value={form.region ?? ''} onChange={(event) => setForm((prev) => ({ ...prev, region: event.target.value ? Number(event.target.value) : undefined }))} />
        </label>
        <label className="flex flex-col gap-1">
          Contexto
          <select aria-label="Contexto" className="rounded border p-2" value={form.context} onChange={(event) => setForm((prev) => ({ ...prev, context: event.target.value as 'urban' | 'rural' }))}>
            <option value="urban">Urbano</option>
            <option value="rural">Rural</option>
          </select>
        </label>
        <label className="flex items-center gap-2">
          <input aria-label="Posee propiedad" type="checkbox" checked={form.owns_property} onChange={(event) => setForm((prev) => ({ ...prev, owns_property: event.target.checked }))} />
          Ya tengo propiedad
        </label>
        <button className="rounded bg-minvuBlue px-4 py-2 font-semibold text-white md:col-span-2" type="submit">Ver recomendaciones</button>
      </form>
    </section>
  )
}
