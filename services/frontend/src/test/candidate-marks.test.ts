import { describe, it, expect } from 'vitest'

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

describe('computeCandidateMarks', () => {
  const emptyGrid = Array.from({ length: 9 }, () => Array(9).fill(0))

  it('returns all candidates for empty grid', () => {
    const marks = computeCandidateMarks(emptyGrid)
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        expect(marks[r][c]).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9])
      }
    }
  })

  it('removes candidates in same row', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[0][0] = 5
    const marks = computeCandidateMarks(grid)

    for (let c = 0; c < 9; c++) {
      expect(marks[0][c]).not.toContain(5)
    }
    expect(marks[1][4]).toContain(5)
  })

  it('removes candidates in same column', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[0][0] = 7
    const marks = computeCandidateMarks(grid)

    for (let r = 0; r < 9; r++) {
      expect(marks[r][0]).not.toContain(7)
    }
    expect(marks[4][4]).toContain(7)
  })

  it('removes candidates in same 3x3 box', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[0][0] = 3
    const marks = computeCandidateMarks(grid)

    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 3; c++) {
        expect(marks[r][c]).not.toContain(3)
      }
    }
    expect(marks[3][3]).toContain(3)
  })

  it('handles filled cells correctly', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[4][4] = 5
    const marks = computeCandidateMarks(grid)

    expect(marks[4][4]).toEqual([])
  })

  it('computes candidates for partially filled grid', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[0] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    grid[8][0] = 9
    const marks = computeCandidateMarks(grid)

    expect(marks[0][8]).toEqual([9])
    expect(marks[1][0]).not.toContain(1)
    expect(marks[1][0]).not.toContain(9)
  })

  it('respects all three sudoku constraints', () => {
    const grid = emptyGrid.map(row => [...row])
    grid[1][0] = 1
    grid[0][1] = 2
    grid[1][1] = 3
    const marks = computeCandidateMarks(grid)

    expect(marks[0][0]).not.toContain(1)
    expect(marks[0][0]).not.toContain(2)
    expect(marks[0][0]).not.toContain(3)
    expect(marks[0][0]).toContain(4)
  })
})
