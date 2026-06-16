import type {
  CombinationResponse,
  EligibilityRequest,
  EligibilityResponse,
  GeneratedPlan,
  PostulationCall,
  Project,
  RegionOption,
  Subsidy,
} from '../types/api'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  })

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`)
  }

  return (await response.json()) as T
}

export const checkEligibility = (payload: EligibilityRequest) =>
  apiFetch<EligibilityResponse>('/eligibility/check', {
    method: 'POST',
    body: JSON.stringify(payload),
  })

export const combineSubsidies = (selected_subsidies: string[]) =>
  apiFetch<CombinationResponse>('/eligibility/combine', {
    method: 'POST',
    body: JSON.stringify({ selected_subsidies }),
  })

export const listSubsidies = () => apiFetch<Subsidy[]>('/subsidies')

export const generatePlans = (baseline: EligibilityRequest, scenarios: Array<{ name: string; savings_delta_uf: number; income_override?: number }>) =>
  apiFetch<{ plans: GeneratedPlan[] }>('/plans/generate', {
    method: 'POST',
    body: JSON.stringify({ baseline, scenarios }),
  })

export const listProjects = (query: URLSearchParams) => apiFetch<Project[]>(`/projects?${query.toString()}`)

export const listRegions = () => apiFetch<RegionOption[]>('/projects/regions')

export const listCalls = () => apiFetch<PostulationCall[]>('/calls')
