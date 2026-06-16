import type { RegionOption } from '../types/api'
import locationData from '../data/regiones_comunas.json'

export interface LocationData {
  regions: RegionOption[]
  communesByRegionId: Record<number, string[]>
  loading: boolean
  error: string | null
}

const regions: RegionOption[] = locationData.regions.map((r) => ({
  id: parseInt(r.number, 10),
  name: r.name,
}))

const communesByRegionId: Record<number, string[]> = {}
for (const r of locationData.regions) {
  communesByRegionId[parseInt(r.number, 10)] = r.communes.map((c) => c.name).sort()
}

export function useLocationData(): LocationData {
  return { regions, communesByRegionId, loading: false, error: null }
}
