import { Navigate, Route, Routes } from 'react-router-dom'

import { Layout } from './components/Layout'
import { CallsPage } from './pages/CallsPage'
import { HomePage } from './pages/HomePage'
import { PlansPage } from './pages/PlansPage'
import { ProjectsPage } from './pages/ProjectsPage'
import { ResultsPage } from './pages/ResultsPage'
import { SubsidyDetailPage } from './pages/SubsidyDetailPage'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/plans" element={<PlansPage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/subsidy/:id" element={<SubsidyDetailPage />} />
        <Route path="/calls" element={<CallsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}

export default App
