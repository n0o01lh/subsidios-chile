import { useState } from 'react'
import type { FormEvent } from 'react'

import { generatePlans } from '../services/api'
import type { EligibilityRequest, GeneratedPlan } from '../types/api'

const STORAGE_KEY = 'subsidios-plans'

const baseline: EligibilityRequest = {
  frs_score: 9000,
  monthly_household_income: 650000,
  family_members: 3,
  current_savings_uf: 20,
  region: 13,
  owns_property: false,
  age: 30,
  context: 'urban',
}

export function PlansPage() {
  const [savingsDelta, setSavingsDelta] = useState(10)
  const [incomeOverride, setIncomeOverride] = useState(700000)
  const [plans, setPlans] = useState<GeneratedPlan[]>(() => {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as GeneratedPlan[]) : []
  })

  const onGenerate = async (event: FormEvent) => {
    event.preventDefault()
    const response = await generatePlans(baseline, [
      { name: 'Plan B', savings_delta_uf: savingsDelta },
      { name: 'Plan C', savings_delta_uf: 0, income_override: incomeOverride },
    ])
    setPlans(response.plans)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(response.plans))
  }

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-minvuBlue">Comparador de planes de postulación</h1>
      <form className="grid gap-4 rounded bg-white p-4 shadow md:grid-cols-2" onSubmit={onGenerate}>
        <label className="flex flex-col gap-1">
          Plan B: ahorro adicional (UF)
          <input className="rounded border p-2" type="number" min={0} value={savingsDelta} onChange={(event) => setSavingsDelta(Number(event.target.value))} />
        </label>
        <label className="flex flex-col gap-1">
          Plan C: ingreso mensual nuevo (CLP)
          <input className="rounded border p-2" type="number" min={0} value={incomeOverride} onChange={(event) => setIncomeOverride(Number(event.target.value))} />
        </label>
        <button className="rounded bg-minvuBlue px-4 py-2 text-white md:col-span-2" type="submit">Generar y comparar</button>
      </form>

      <div className="overflow-x-auto rounded bg-white shadow">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-100">
            <tr>
              <th className="px-3 py-2">Plan</th>
              <th className="px-3 py-2">Subsidio recomendado</th>
              <th className="px-3 py-2">Beneficio total UF</th>
              <th className="px-3 py-2">Espera estimada</th>
            </tr>
          </thead>
          <tbody>
            {plans.map((plan) => (
              <tr key={plan.name} className="border-t">
                <td className="px-3 py-2">{plan.name}</td>
                <td className="px-3 py-2">{plan.result.best_match_subsidy_id ?? 'Sin match'}</td>
                <td className="px-3 py-2">{plan.total_benefit_uf}</td>
                <td className="px-3 py-2">{plan.estimated_waiting_time_months} meses</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
