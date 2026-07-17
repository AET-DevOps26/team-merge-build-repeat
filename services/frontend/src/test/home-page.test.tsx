import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '@/src/pages/HomePage'
import type { ReactNode } from 'react'

const mockAuthContext = {
  user: { id: 'user-1' },
  accessToken: 'test-token',
}

vi.mock('@/src/auth/auth-context', () => ({
  useAuth: () => mockAuthContext,
}))

vi.mock('@/src/game-context', () => ({
  useGame: () => ({ activeGameId: null, setActiveGameId: vi.fn() }),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

vi.mock('@/components/navigation', () => ({
  Header: () => <div data-testid="header">Header</div>,
  BottomNav: () => <div data-testid="bottom-nav">Bottom Nav</div>,
}))

describe('HomePage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch = vi.fn()
  })

  it('renders the page title', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    expect(screen.getByText('PAULANA')).toBeInTheDocument()
    expect(screen.getByText('ZUDOKYU')).toBeInTheDocument()
  })

  it('renders difficulty buttons', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    expect(screen.getByRole('button', { name: /easy/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /medium/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /hard/i })).toBeInTheDocument()
  })

  it('renders template ID input', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    const input = screen.getByPlaceholderText(/xxxxxxxx/i)
    expect(input).toBeInTheDocument()
  })

  it('renders continue button', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    expect(screen.getByRole('button', { name: /continue/i })).toBeInTheDocument()
  })

  it('validates UUID format in template ID input', async () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    const input = screen.getByPlaceholderText(/xxxxxxxx/i) as HTMLInputElement
    const loadButton = screen.getByRole('button', { name: /load/i })

    fireEvent.change(input, { target: { value: 'invalid' } })
    expect(loadButton).toBeDisabled()

    fireEvent.change(input, { target: { value: '12345678-9012-3456-7890-123456789012' } })
    expect(loadButton).not.toBeDisabled()
  })

  it('renders header and footer', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    expect(screen.getByTestId('header')).toBeInTheDocument()
    expect(screen.getByTestId('bottom-nav')).toBeInTheDocument()
  })

  it('load button is disabled without valid UUID', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    const loadButton = screen.getByRole('button', { name: /load/i })
    expect(loadButton).toBeDisabled()
  })
})
