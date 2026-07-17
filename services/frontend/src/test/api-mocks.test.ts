import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('API fetch utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch = vi.fn()
  })

  describe('game fetching', () => {
    it('should fetch game with correct headers', async () => {
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ gameId: '123', templateId: 'template-456' }),
      })
      global.fetch = mockFetch

      const response = await fetch('/application/v1/games/random?difficulty=easy', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer test-token' },
      })

      expect(mockFetch).toHaveBeenCalledWith(
        '/application/v1/games/random?difficulty=easy',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token',
          }),
        })
      )
      const data = await response.json()
      expect(data).toEqual({ gameId: '123', templateId: 'template-456' })
    })

    it('should handle game fetch errors', async () => {
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        status: 404,
      })
      global.fetch = mockFetch

      const response = await fetch('/application/v1/games/123')
      expect(response.ok).toBe(false)
      expect(response.status).toBe(404)
    })
  })

  describe('sudoku operations', () => {
    it('should fetch sudoku puzzle', async () => {
      const mockPuzzle = Array.from({ length: 9 }, () => Array(9).fill(0))
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ sudoku: mockPuzzle }),
      })
      global.fetch = mockFetch

      const response = await fetch('/game-engine/sudoku')
      const data = await response.json()

      expect(data.sudoku).toEqual(mockPuzzle)
    })

    it('should post solution request', async () => {
      const mockSolution = Array.from({ length: 9 }, () => Array(9).fill(1))
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ sudoku: mockSolution }),
      })
      global.fetch = mockFetch

      const puzzle = Array.from({ length: 9 }, () => Array(9).fill(0))
      const response = await fetch('/game-engine/solution', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sudoku: puzzle }),
      })

      expect(mockFetch).toHaveBeenCalledWith(
        '/game-engine/solution',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ sudoku: puzzle }),
        })
      )
      const data = await response.json()
      expect(data.sudoku).toEqual(mockSolution)
    })
  })

  describe('game state operations', () => {
    it('should fetch game history', async () => {
      const mockHistory = [
        { row: 0, col: 0, value: 5, createdAt: '2024-01-01T00:00:00Z' },
      ]
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory,
      })
      global.fetch = mockFetch

      const response = await fetch('/application/v1/games/123/history', {
        headers: { 'Authorization': 'Bearer token' },
      })
      const data = await response.json()

      expect(data).toEqual(mockHistory)
    })

    it('should post to game history', async () => {
      const mockFetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        status: 204,
      })
      global.fetch = mockFetch

      const move = { row: 0, col: 0, value: 5 }
      const response = await fetch('/application/v1/games/123/history', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer token',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(move),
      })

      expect(mockFetch).toHaveBeenCalledWith(
        '/application/v1/games/123/history',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(move),
        })
      )
      expect(response.status).toBe(204)
    })
  })
})
