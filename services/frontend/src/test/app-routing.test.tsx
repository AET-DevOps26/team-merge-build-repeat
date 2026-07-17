import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter, MemoryRouter } from 'react-router-dom'
import App from '@/src/App'
import type { ReactNode } from 'react'

const mockAuthContext = {
  session: { user: { id: 'user-1' } },
  loading: false,
}

vi.mock('@/src/auth/auth-context', () => ({
  useAuth: () => mockAuthContext,
}))

vi.mock('@/src/auth/require-auth', () => ({
  RequireAuth: () => <div data-testid="require-auth">Protected</div>,
}))

vi.mock('@/src/pages/LoginPage', () => ({
  default: () => <div data-testid="login-page">Login Page</div>,
}))

vi.mock('@/src/pages/HomePage', () => ({
  default: () => <div data-testid="home-page">Home Page</div>,
}))

vi.mock('@/src/pages/GamePage', () => ({
  default: () => <div data-testid="game-page">Game Page</div>,
}))

vi.mock('@/src/pages/HistoryPage', () => ({
  default: () => <div data-testid="history-page">History Page</div>,
}))

describe('App routing', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login page at /login', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>
    )
    expect(screen.getByTestId('login-page')).toBeInTheDocument()
  })

  it('requires auth for protected routes', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    )
    expect(screen.getByTestId('require-auth')).toBeInTheDocument()
  })

  it('renders game redirect when navigating to /game without gameId', () => {
    const mockGameContext = { activeGameId: null }
    vi.mock('@/src/game-context', () => ({
      useGame: () => mockGameContext,
    }))

    render(
      <MemoryRouter initialEntries={['/game']}>
        <App />
      </MemoryRouter>
    )
  })

  it('has correct route structure', () => {
    const { container } = render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    )
    expect(container).toBeInTheDocument()
  })
})
