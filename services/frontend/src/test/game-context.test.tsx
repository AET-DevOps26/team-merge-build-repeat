import {describe, it, expect, beforeEach, vi} from 'vitest'
import {render, screen} from '@testing-library/react'
import {GameProvider, useGame} from '@/src/game-context'
import type {ReactNode} from 'react'

const mockAuthContext = {
    session: {user: {id: 'user-1'}},
    loading: false,
}

vi.mock('@/src/auth/auth-context', () => ({
    useAuth: () => mockAuthContext,
}))

function TestComponent() {
    try {
        const {activeGameId, setActiveGameId} = useGame()
        return (
            <div>
                <div data-testid="active-game-id">{activeGameId || 'none'}</div>
                <button onClick={() => setActiveGameId('game-123')}>
                    Set Game
                </button>
                <button onClick={() => setActiveGameId(null)}>
                    Clear Game
                </button>
            </div>
        )
    } catch (e) {
        return <div data-testid="error">{(e as Error).message}</div>
    }
}

describe('GameProvider', () => {
    beforeEach(() => {
        localStorage.clear()
        vi.clearAllMocks()
    })

    it('provides context to children', () => {
        render(
            <GameProvider>
                <TestComponent/>
            </GameProvider>
        )
        expect(screen.getByTestId('active-game-id')).toBeInTheDocument()
    })

    it('throws error when useGame is used outside provider', () => {
        render(<TestComponent/>)
        expect(screen.getByTestId('error')).toHaveTextContent(
            'useGame must be used inside GameProvider'
        )
    })
})
