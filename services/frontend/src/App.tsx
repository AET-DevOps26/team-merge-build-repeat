import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import GamePage from './pages/GamePage'
import StatsPage from './pages/StatsPage'
import AIPage from './pages/AIPage'
import RankPage from './pages/RankPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/game" element={<GamePage />} />
      <Route path="/stats" element={<StatsPage />} />
      <Route path="/ai" element={<AIPage />} />
      <Route path="/rank" element={<RankPage />} />
    </Routes>
  )
}
