export interface EligibilityRequest {
  frs_score: number
  monthly_household_income?: number
  family_members?: number
  current_savings_uf?: number
  region?: number
  owns_property: boolean
  age?: number
  context: 'urban' | 'rural'
}

export interface EligibilityResult {
  subsidy_id: string
  subsidy_name: string
  eligible: boolean
  benefit_uf: number
  requirement_gaps: string[]
  estimated_timeline_months: number
}

export interface EligibilityResponse {
  best_match_subsidy_id: string | null
  ranked_subsidies: EligibilityResult[]
}

export interface CombinationResponse {
  valid: boolean
  total_package_uf: number
  warnings: string[]
  applied_rules: string[]
}

export interface Subsidy {
  id: string
  name: string
  decree: string
  target: string
  frs_min: number
  frs_max: number
  benefit_uf: number
  required_savings_uf: number
  max_property_value_uf: number
  mortgage_allowed: boolean
  mortgage_required: boolean
  modality: string
  region_availability: number[]
  postulation_periods: string[]
  compatible_savings_instruments: string[]
  compatible_with: string[]
}

export interface GeneratedPlan {
  name: string
  total_benefit_uf: number
  estimated_waiting_time_months: number
  steps: string[]
  result: EligibilityResponse
}

export interface Project {
  id: number
  name: string
  region: number
  commune: string
  subsidy_program: string
  available_units: number
  min_price_uf: number
  max_price_uf: number
  bedrooms: number
  address: string
  source_url: string
}

export interface PostulationCall {
  id: number
  subsidy_program: string
  region: number
  opening_date: string
  closing_date: string
  available_quotas: number
  requirements: string
  source_url: string
}
