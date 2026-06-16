import { Link, NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Inicio' },
  { to: '/results', label: 'Resultados' },
  { to: '/plans', label: 'Planes' },
  { to: '/projects', label: 'Proyectos' },
  { to: '/calls', label: 'Llamados' },
]

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="bg-minvuBlue text-white shadow">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <Link to="/" className="font-semibold">Subsidios Chile</Link>
          <ul className="flex gap-4 text-sm">
            {links.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) => (isActive ? 'font-semibold underline' : 'opacity-90 hover:opacity-100')}
                >
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </header>
      <main className="mx-auto max-w-6xl p-4">{children}</main>
      <footer className="border-t bg-white px-4 py-4 text-center text-sm text-slate-600">
        Esta herramienta es orientativa. Siempre consulte con su SERVIU regional.
      </footer>
    </div>
  )
}
