import { describe, it, expect } from 'vitest'

const EMPTY_GRID = Array.from({ length: 9 }, () => Array(9).fill(0))

type SingleMove =
  | { type: "number"; row: number; col: number; value: number }
  | { type: "pencil"; row: number; col: number; value: number; action: "ADD" | "REMOVE" }

type Move =
  | SingleMove
  | { type: "batch"; moves: SingleMove[] }

function computeCandidateMarks(grid: number[][]): number[][][] {
  const marks: number[][][] = Array.from({ length: 9 }, () =>
    Array.from({ length: 9 }, () => [] as number[])
  )
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (grid[r][c]) continue
      const boxR = Math.floor(r / 3) * 3
      const boxC = Math.floor(c / 3) * 3
      for (let n = 1; n <= 9; n++) {
        const inRow = grid[r].includes(n)
        const inCol = grid.some(row => row[c] === n)
        const inBox = grid.slice(boxR, boxR + 3).some(row => row.slice(boxC, boxC + 3).includes(n))
        if (!inRow && !inCol && !inBox)
          marks[r][c].push(n)
      }
    }
  }
  return marks
}

describe('Grid state management', () => {
  it('applies number moves to grid', () => {
    const puzzle = EMPTY_GRID.map(row => [...row])
    const moves: Move[] = [
      { type: "number", row: 0, col: 0, value: 5 },
      { type: "number", row: 1, col: 1, value: 3 },
    ]

    const grid = puzzle.map(row => [...row])
    for (const move of moves) {
      if (move.type === "number") {
        grid[move.row][move.col] = move.value
      }
    }

    expect(grid[0][0]).toBe(5)
    expect(grid[1][1]).toBe(3)
  })

  it('handles batch moves', () => {
    const puzzle = EMPTY_GRID.map(row => [...row])
    const moves: Move[] = [
      {
        type: "batch",
        moves: [
          { type: "number", row: 0, col: 0, value: 1 },
          { type: "number", row: 0, col: 1, value: 2 },
          { type: "number", row: 0, col: 2, value: 3 },
        ],
      },
    ]

    const grid = puzzle.map(row => [...row])
    for (const move of moves) {
      if (move.type === "batch") {
        for (const m of move.moves) {
          grid[m.row][m.col] = m.value
        }
      }
    }

    expect(grid[0]).toEqual([1, 2, 3, 0, 0, 0, 0, 0, 0])
  })

  it('handles pencil mark add action', () => {
    const pencilMarks: number[][][] = Array.from({ length: 9 }, () =>
      Array.from({ length: 9 }, () => [] as number[])
    )

    const move: Move = { type: "pencil", row: 0, col: 0, value: 5, action: "ADD" }
    if (move.type === "pencil" && move.action === "ADD") {
      const marks = pencilMarks[move.row][move.col]
      if (!marks.includes(move.value)) {
        pencilMarks[move.row][move.col] = [...marks, move.value].sort((a, b) => a - b)
      }
    }

    expect(pencilMarks[0][0]).toContain(5)
  })

  it('handles pencil mark remove action', () => {
    const pencilMarks: number[][][] = Array.from({ length: 9 }, () =>
      Array.from({ length: 9 }, () => [1, 2, 3])
    )

    const move: Move = { type: "pencil", row: 0, col: 0, value: 2, action: "REMOVE" }
    if (move.type === "pencil" && move.action === "REMOVE") {
      pencilMarks[move.row][move.col] = pencilMarks[move.row][move.col].filter(
        mark => mark !== move.value
      )
    }

    expect(pencilMarks[0][0]).toEqual([1, 3])
    expect(pencilMarks[0][0]).not.toContain(2)
  })

  it('undoes moves by removing last move', () => {
    const moves: Move[] = [
      { type: "number", row: 0, col: 0, value: 5 },
      { type: "number", row: 1, col: 1, value: 3 },
    ]

    const grid = EMPTY_GRID.map(row => [...row])
    for (const move of moves) {
      if (move.type === "number") {
        grid[move.row][move.col] = move.value
      }
    }

    moves.pop()
    const grid2 = EMPTY_GRID.map(row => [...row])
    for (const move of moves) {
      if (move.type === "number") {
        grid2[move.row][move.col] = move.value
      }
    }

    expect(grid2[1][1]).toBe(0)
    expect(grid2[0][0]).toBe(5)
  })

  it('tracks given cells correctly', () => {
    const puzzle = EMPTY_GRID.map(row => [...row])
    puzzle[0][0] = 5
    puzzle[1][1] = 3

    const givenCells = puzzle.map(row => row.map(cell => Boolean(cell)))

    expect(givenCells[0][0]).toBe(true)
    expect(givenCells[1][1]).toBe(true)
    expect(givenCells[0][1]).toBe(false)
  })

  it('computes candidate marks respecting filled cells', () => {
    const puzzle = EMPTY_GRID.map(row => [...row])
    puzzle[0][0] = 5
    const marks = computeCandidateMarks(puzzle)

    expect(marks[0][0]).toEqual([])
    expect(marks[0][1]).not.toContain(5)
    expect(marks[1][0]).not.toContain(5)
  })
})
