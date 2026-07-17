import { Routes, Route, Navigate } from 'react-router-dom'
import HomePage from './pages/HomePage'
import GamePage from './pages/GamePage'
import LoginPage from './pages/LoginPage'
import HistoryPage from './pages/HistoryPage'
import { RequireAuth } from './auth/require-auth'
import { useGame } from './game-context'

function GameRedirect() {
  const { activeGameId } = useGame()
  if (activeGameId) return <Navigate to={`/game/${activeGameId}`} replace />
  return <Navigate to="/" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<RequireAuth />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/game/:gameId" element={<GamePage />} />
        <Route path="/game" element={<GameRedirect />} />
      </Route>
    </Routes>
  )
}
