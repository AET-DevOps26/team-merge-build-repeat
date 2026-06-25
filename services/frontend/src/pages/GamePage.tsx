import { useState, useEffect, useCallback, useMemo } from "react"
import { Header, BottomNav } from "@/components/navigation"
import { SudokuGrid, NumberPad } from "@/components/game"
import { GameChat } from "@/components/chat"

const EMPTY_GRID = Array.from({ length: 9 }, () => Array(9).fill(0))

// Fixed game id used for the chat until per-game ids are wired up.
const GAME_ID = "00000000-0000-0000-0000-000000000001"

type SingleMove =
  | { type: "number"; row: number; col: number; value: number }
  | { type: "pencil"; row: number; col: number; value: number }

type Move =
  | SingleMove
  | { type: "batch"; moves: SingleMove[] }

function computeInitialMarks(puzzle: number[][]): number[][][] {
  const marks: number[][][] = Array.from({ length: 9 }, () =>
    Array.from({ length: 9 }, () => [] as number[])
  )
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (puzzle[r][c]) continue
      const boxR = Math.floor(r / 3) * 3
      const boxC = Math.floor(c / 3) * 3
      for (let n = 1; n <= 9; n++) {
        const inRow = puzzle[r].includes(n)
        const inCol = puzzle.some(row => row[c] === n)
        const inBox = puzzle.slice(boxR, boxR + 3).some(row => row.slice(boxC, boxC + 3).includes(n))
        if (!inRow && !inCol && !inBox)
          marks[r][c].push(n)
      }
    }
  }
  return marks
}

async function fetchSudoku(): Promise<number[][]> {
  const res = await fetch("/api/game-engine/sudoku")
  if (!res.ok) throw new Error(`Failed to fetch sudoku: ${res.status}`)
  const data = await res.json()
  return data.sudoku
}

async function fetchSolution(puzzle: number[][]): Promise<number[][]> {
  const res = await fetch("/api/game-engine/solution", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sudoku: puzzle })
  })
  if (!res.ok) throw new Error(`Failed to fetch solution: ${res.status}`)
  const data = await res.json()
  return data.sudoku
}

export default function GamePage() {
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null)
  const [puzzle, setPuzzle] = useState<number[][]>(EMPTY_GRID)
  const [initialMarks, setInitialMarks] = useState<number[][][]>([])
  const [moves, setMoves] = useState<Move[]>([])
  const [redoMoves, setRedoMoves] = useState<Move[]>([])
  const [pencilMode, setPencilMode] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [wrongCells, setWrongCells] = useState<Set<string>>(new Set())
  const [correctCells, setCorrectCells] = useState<Set<string>>(new Set())

  const givenCells = useMemo(
    () => puzzle.map(row => row.map(cell => Boolean(cell))),
    [puzzle]
  )

  const { grid, pencilMarks } = useMemo(() => {
    const g = puzzle.map(row => [...row])
    const p: number[][][] = Array.from({ length: 9 }, (_, r) =>
      Array.from({ length: 9 }, (_, c) => [...(initialMarks[r]?.[c] ?? [])])
    )
    const applyMove = (m: Move) => {
      if (m.type === "batch") {
        for (const batchMove of m.moves) applyMove(batchMove)
      } else if (m.type === "number") {
        g[m.row][m.col] = m.value
        p[m.row][m.col] = []
        if (m.value !== 0) {
          const boxR = Math.floor(m.row / 3) * 3
          const boxC = Math.floor(m.col / 3) * 3
          for (let i = 0; i < 9; i++) {
            const peers: [number, number][] = [
              [m.row, i],
              [i, m.col],
              [boxR + Math.floor(i / 3), boxC + (i % 3)],
            ]
            for (const [pr, pc] of peers)
              p[pr][pc] = p[pr][pc].filter(mark => mark !== m.value)
          }
        }
      } else {
        const marks = p[m.row][m.col]
        const idx = marks.indexOf(m.value)
        p[m.row][m.col] = idx === -1
          ? [...marks, m.value].sort((a, b) => a - b)
          : marks.filter(mark => mark !== m.value)
      }
    }

    for (const move of moves) applyMove(move)
    return { grid: g, pencilMarks: p }
  }, [puzzle, moves, initialMarks])

  const loadNewGame = useCallback(async () => {
    setLoading(true)
    setError(null)
    setSelectedCell(null)
    setMoves([])
    setPencilMode(false)
    setWrongCells(new Set())
    setCorrectCells(new Set())
    try {
      const raw = await fetchSudoku()
      const sudoku = raw.map(row => row.map(cell => cell ?? 0))
      setPuzzle(sudoku)
      setInitialMarks(computeInitialMarks(sudoku))
      setMoves([])
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load puzzle")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadNewGame()
  }, [loadNewGame])

  const handleCellClick = (row: number, col: number) => {
    if (!givenCells[row][col]) setSelectedCell({ row, col })
  }

  const handleNumberClick = (num: number) => {
    if (!selectedCell || givenCells[selectedCell.row][selectedCell.col]) return
    const key = `${selectedCell.row},${selectedCell.col}`
    setWrongCells(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
    setCorrectCells(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
    setRedoMoves([])
    setMoves(prev => [...prev, {
      type: pencilMode ? "pencil" : "number",
      row: selectedCell.row,
      col: selectedCell.col,
      value: num,
    }])
  }

  const handleDelete = () => {
    if (!selectedCell || givenCells[selectedCell.row][selectedCell.col]) return
    const key = `${selectedCell.row},${selectedCell.col}`
    setWrongCells(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
    setCorrectCells(prev => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
    setRedoMoves([])
    setMoves(prev => [...prev, { type: "number", row: selectedCell.row, col: selectedCell.col, value: 0 }])
  }

  const handleUndo = () => {
    if (moves.length === 0) return
    const lastMove = moves[moves.length - 1]
    const cellsToUnhighlight = new Set<string>()

    if (lastMove.type === "batch") {
      for (const move of lastMove.moves) {
        if (move.type === "number") {
          cellsToUnhighlight.add(`${move.row},${move.col}`)
        }
      }
    } else if (lastMove.type === "number") {
      cellsToUnhighlight.add(`${lastMove.row},${lastMove.col}`)
    }

    if (cellsToUnhighlight.size > 0) {
      setWrongCells(prev => {
        const next = new Set(prev)
        cellsToUnhighlight.forEach(cell => next.delete(cell))
        return next
      })
      setCorrectCells(prev => {
        const next = new Set(prev)
        cellsToUnhighlight.forEach(cell => next.delete(cell))
        return next
      })
    }

    setMoves(prev => {
      const newMoves = prev.slice(0, -1)
      setRedoMoves([lastMove])
      return newMoves
    })
  }

  const handleRedo = () => {
    if (redoMoves.length === 0) return
    const moveToRedo = redoMoves[0]
    setRedoMoves([])
    setMoves(prev => [...prev, moveToRedo])
  }

  const handleCheck = useCallback(async () => {
    try {
      const solution = await fetchSolution(puzzle)
      const wrong = new Set<string>()
      const correct = new Set<string>()
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (!givenCells[r][c] && grid[r][c] !== 0) {
            if (grid[r][c] === solution[r][c]) {
              correct.add(`${r},${c}`)
            } else {
              wrong.add(`${r},${c}`)
            }
          }
        }
      }
      setWrongCells(wrong)
      setCorrectCells(correct)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to check solution")
    }
  }, [puzzle, grid, givenCells])

  const handleSolve = useCallback(async () => {
    try {
      const solution = await fetchSolution(puzzle)
      const batchMoves: SingleMove[] = []
      const solvedWrong = new Set<string>()
      const correct = new Set<string>()
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (!givenCells[r][c]) {
            if (grid[r][c] !== solution[r][c]) {
              batchMoves.push({ type: "number", row: r, col: c, value: solution[r][c] })
              if (grid[r][c] !== 0) {
                solvedWrong.add(`${r},${c}`)
              }
            } else if (grid[r][c] !== 0) {
              correct.add(`${r},${c}`)
            }
          }
        }
      }
      if (batchMoves.length === 0) return
      setWrongCells(solvedWrong)
      setCorrectCells(correct)
      setMoves(prev => [...prev, { type: "batch", moves: batchMoves }])
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to solve puzzle")
    }
  }, [puzzle, grid, givenCells])

  return (
    <div className="h-screen bg-background flex flex-col">
      <Header />

      <main className="flex-1 flex flex-row items-stretch px-4 py-4 pb-32 gap-4 min-h-0 overflow-hidden">
        <div className="flex-1 hidden md:flex flex-col min-h-0">
          <GameChat gameId={GAME_ID} board={grid} candidates={pencilMarks} />
        </div>

        <div className="flex items-center justify-center min-h-0 flex-shrink-0">
          <div className="aspect-square h-full max-w-full relative">
            {loading && (
              <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10 rounded">
                <span className="material-symbols-outlined text-accent text-5xl animate-spin">progress_activity</span>
              </div>
            )}
            {error && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-card/90 z-10 rounded gap-3">
                <span className="text-destructive font-bold">{error}</span>
                <button
                  onClick={loadNewGame}
                  className="bg-accent text-white font-bold px-4 py-2 rounded border-2 border-primary shadow-[3px_3px_0px_0px_var(--color-primary)] hover:brightness-110 transition-all"
                >
                  Retry
                </button>
              </div>
            )}
            <SudokuGrid
              grid={grid}
              givenCells={givenCells}
              pencilMarks={pencilMarks}
              selectedCell={selectedCell}
              onCellClick={handleCellClick}
              wrongCells={wrongCells}
              correctCells={correctCells}
            />
          </div>
        </div>

        <div className="flex-1 flex flex-col gap-2 items-center justify-center min-h-0">
          <NumberPad
            onNumberClick={handleNumberClick}
            onDelete={handleDelete}
            onUndo={handleUndo}
            onRedo={handleRedo}
            canUndo={moves.length > 0}
            canRedo={redoMoves.length > 0}
            pencilMode={pencilMode}
            onTogglePencil={() => setPencilMode(m => !m)}
            onCheck={handleCheck}
            onSolve={handleSolve}
          />
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
