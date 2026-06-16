import { useEffect, useState } from 'react'

import { listRegions } from '../services/api'
import type { RegionOption } from '../types/api'

// Raw URL for the juanbrujo gist: regiones y comunas de Chile
// https://gist.github.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd
const GIST_URL =
  'https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/regiones_comunas.json'

interface GistRegion {
  region: string
  region_numero?: string
  region_iso?: string
  comunas: string[]
}

interface GistData {
  regiones: GistRegion[]
}

/**
 * Normalises a region name for fuzzy matching:
 * "Región de Arica y Parinacota" → "arica y parinacota"
 * "La Araucanía"                 → "araucanía"
 */
function normalise(name: string): string {
  return name
    .toLowerCase()
    .replace(/^regi[oó]n\s+(de\s+la?l?\s*|del?\s+)?/i, '')
    .replace(/^la\s+/, '')
    .trim()
}

export interface LocationData {
  regions: RegionOption[]
  communesByRegionId: Record<number, string[]>
  loading: boolean
  error: string | null
}

export function useLocationData(): LocationData {
  const [regions, setRegions] = useState<RegionOption[]>([])
  const [communesByRegionId, setCommunesByRegionId] = useState<Record<number, string[]>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const [backendRegions, gistResponse] = await Promise.all([
          listRegions(),
          fetch(GIST_URL),
        ])

        if (!gistResponse.ok) {
          throw new Error(`Gist fetch failed: ${gistResponse.status}`)
        }

        const gistData = (await gistResponse.json()) as GistData
        const gistRegions: GistRegion[] = gistData.regiones ?? []

        // Build a lookup from normalised name → communes
        const gistLookup = new Map<string, string[]>()
        for (const gr of gistRegions) {
          gistLookup.set(normalise(gr.region), gr.comunas)
        }

        // Map each backend region id to its gist communes
        const byId: Record<number, string[]> = {}
        for (const r of backendRegions) {
          const communes = gistLookup.get(normalise(r.name))
          byId[r.id] = communes ? [...communes].sort() : []
        }

        if (!cancelled) {
          setRegions(backendRegions)
          setCommunesByRegionId(byId)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Error cargando datos de ubicación')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void load()
    return () => {
      cancelled = true
    }
  }, [])

  return { regions, communesByRegionId, loading, error }
}
