import { useState, useEffect, useCallback, useMemo, useRef } from "react"
import { useParams, useLocation, useNavigate } from "react-router-dom"
import { Header, BottomNav } from "@/components/navigation"
import { SudokuGrid, NumberPad } from "@/components/game"
import { GameChat } from "@/components/chat"
import { useAuth } from "@/src/auth/auth-context"
import { useGame } from "@/src/game-context"

const EMPTY_GRID = Array.from({ length: 9 }, () => Array(9).fill(0))

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

type SingleMove =
  | { type: "number"; row: number; col: number; value: number }
  | { type: "pencil"; row: number; col: number; value: number; action: "ADD" | "REMOVE" }

type Move =
  | SingleMove
  | { type: "batch"; moves: SingleMove[] }


async function fetchGameFromApplication(gameId: string, accessToken: string): Promise<{ templateData: number[][]; solutionData: number[][] }> {
  const [templateRes, stateRes] = await Promise.all([
    fetch(`/application/v1/games/${gameId}/template`, {
      headers: { "Authorization": `Bearer ${accessToken}` },
    }),
    fetch(`/application/v1/games/${gameId}/state`, {
      headers: { "Authorization": `Bearer ${accessToken}` },
    }),
  ])
  if (!templateRes.ok || !stateRes.ok) {
    const status = !templateRes.ok ? templateRes.status : stateRes.status
    const err = new Error(`Failed to fetch game: ${status}`)
    ;(err as any).status = status
    throw err
  }
  const templateData = await templateRes.json()
  const stateData = await stateRes.json()
  return { templateData, solutionData: stateData }
}

async function fetchSudoku(): Promise<number[][]> {
  const res = await fetch("/game-engine/sudoku")
  if (!res.ok) throw new Error(`Failed to fetch sudoku: ${res.status}`)
  const data = await res.json()
  return data.sudoku
}

async function fetchSolution(puzzle: number[][]): Promise<number[][]> {
  const res = await fetch("/game-engine/solution", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sudoku: puzzle })
  })
  if (!res.ok) throw new Error(`Failed to fetch solution: ${res.status}`)
  const data = await res.json()
  return data.sudoku
}

async function fetchGameHistory(gameId: string, accessToken: string): Promise<Array<{ row: number; col: number; value: number; createdAt: string | null }>> {
  const res = await fetch(`/application/v1/games/${gameId}/history`, {
    headers: { "Authorization": `Bearer ${accessToken}` },
  })
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.status}`)
  const data = await res.json()
  return data
}

async function fetchGameInfo(gameId: string, accessToken: string): Promise<{ templateId: string }> {
  const res = await fetch(`/application/v1/games/${gameId}/info`, {
    headers: { "Authorization": `Bearer ${accessToken}` },
  })
  if (!res.ok) throw new Error(`Failed to fetch game info: ${res.status}`)
  const data = await res.json()
  return data
}

type PencilMarkHistoryEntry = { row: number; col: number; value: number; action: "ADD" | "REMOVE"; initial: boolean; createdAt: string | null }

async function fetchPencilMarkHistory(gameId: string, accessToken: string): Promise<PencilMarkHistoryEntry[]> {
  const res = await fetch(`/application/v1/games/${gameId}/pencil-mark-history`, {
    headers: { "Authorization": `Bearer ${accessToken}` },
  })
  if (!res.ok) throw new Error(`Failed to fetch pencil mark history: ${res.status}`)
  return res.json()
}

async function sendGameMutation(path: string, accessToken: string | null, method: "POST" | "DELETE", body?: object): Promise<void> {
  const res = await fetch(path, {
    method,
    headers: {
      ...(body ? { "Content-Type": "application/json" } : {}),
      "Authorization": `Bearer ${accessToken}`,
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  })
  if (!res.ok) throw new Error(`Game update failed: ${res.status}`)
  if (method === "POST" && path.endsWith("/history") && await res.json() !== true) {
    throw new Error("Game update was rejected")
  }
}

async function savePencilMarkHistory(gameId: string, accessToken: string | null, row: number, col: number, value: number, action: "ADD" | "REMOVE", initial: boolean): Promise<void> {
  await sendGameMutation(`/application/v1/games/${gameId}/pencil-mark-history`, accessToken, "POST", { row, column: col, value, action, initial })
}

export default function GamePage() {
  const { gameId: gameIdParam } = useParams<{ gameId: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const { accessToken } = useAuth()
  const { setActiveGameId } = useGame()
  const [gameId, setGameId] = useState<string | null>(gameIdParam || null)
  const [templateId, setTemplateId] = useState<string | null>((location.state as any)?.templateId || null)
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null)
  const [puzzle, setPuzzle] = useState<number[][]>(EMPTY_GRID)
  const [initialMarks, setInitialMarks] = useState<number[][][]>([])
  const [moves, setMoves] = useState<Move[]>([])
  const [initialMoveCount, setInitialMoveCount] = useState(0)
  const [redoMoves, setRedoMoves] = useState<Move[]>([])
  const [pencilMode, setPencilMode] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [wrongCells, setWrongCells] = useState<Set<string>>(new Set())
  const [correctCells, setCorrectCells] = useState<Set<string>>(new Set())
  const [copyFeedback, setCopyFeedback] = useState(false)
  const prevFilledRef = useRef(false)
  const mutationQueueRef = useRef<Promise<void>>(Promise.resolve())

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
      if (gameId) {
        // Load game from Application Service
        const gameData = await fetchGameFromApplication(gameId, accessToken)
        const puzzle = gameData.templateData.map(row => row.map(cell => cell ?? 0))
        setPuzzle(puzzle)
        setInitialMarks(computeInitialMarks(puzzle))

        // Fetch templateId if not set
        if (!templateId) {
          const gameInfo = await fetchGameInfo(gameId, accessToken)
          setTemplateId(gameInfo.templateId)
        }

        // Fetch both histories and merge in chronological order
        const [history, pencilHistory] = await Promise.all([
          fetchGameHistory(gameId, accessToken),
          fetchPencilMarkHistory(gameId, accessToken),
        ])

        type TimestampedMove = Move & { createdAt: string | null }
        const numberedMoves: TimestampedMove[] = history.map(h => ({
          type: "number" as const, row: h.row, col: h.col, value: h.value, createdAt: h.createdAt,
        }))
        const pencilMoves: TimestampedMove[] = pencilHistory
          .filter(h => !h.initial)
          .map(h => ({
            type: "pencil" as const, row: h.row, col: h.col, value: h.value, action: h.action, createdAt: h.createdAt,
          }))

        const merged = [...numberedMoves, ...pencilMoves]
          .sort((a, b) => {
            if (!a.createdAt) return -1
            if (!b.createdAt) return 1
            return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
          })
          .map(({ createdAt: _, ...move }) => move as Move)

        // Pre-sync fill state so the auto-check effect doesn't fire on load
        const loadedGrid = puzzle.map(row => [...row])
        for (const move of merged) {
          if (move.type === "number") loadedGrid[move.row][move.col] = move.value
          else if (move.type === "batch") {
            for (const m of move.moves) loadedGrid[m.row][m.col] = m.value
          }
        }
        prevFilledRef.current = loadedGrid.every(row => row.every(cell => cell !== 0))

        setInitialMoveCount(0)
        setMoves(merged)
        setActiveGameId(gameId)
      } else {
        // Fallback: Load from Game Engine (old behavior)
        const raw = await fetchSudoku()
        const puzzle = raw.map(row => row.map(cell => cell ?? 0))
        setPuzzle(puzzle)
        setMoves([])
      }
    } catch (e) {
      const status = (e as any)?.status
      if (status === 403) {
        navigate("/", { replace: true })
        return
      }
      setError(e instanceof Error ? e.message : "Failed to load puzzle")
    } finally {
      setLoading(false)
    }
  }, [gameId, accessToken, templateId, setActiveGameId, navigate])

  useEffect(() => {
    loadNewGame()
  }, [loadNewGame])

  const enqueueMutation = useCallback((mutation: () => Promise<void>) => {
    mutationQueueRef.current = mutationQueueRef.current
      .then(mutation)
      .catch(async (err) => {
        const message = err instanceof Error ? err.message : "Failed to update game"
        await loadNewGame()
        setError(message)
      })
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

    if (pencilMode) {
      const action = pencilMarks[selectedCell.row][selectedCell.col].includes(num) ? "REMOVE" : "ADD"
      const newMove: Move = { type: "pencil", row: selectedCell.row, col: selectedCell.col, value: num, action }
      setMoves(prev => [...prev, newMove])
      if (gameId) {
        enqueueMutation(() => savePencilMarkHistory(gameId, accessToken, selectedCell.row, selectedCell.col, num, action, false))
      }
      return
    }

    const newMove: Move = { type: "number", row: selectedCell.row, col: selectedCell.col, value: num }
    setMoves(prev => [...prev, newMove])

    if (!pencilMode && gameId) {
      enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "POST", {
        row: selectedCell.row, col: selectedCell.col, value: num,
      }))
    }
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

    if (gameId) {
      enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "POST", {
        row: selectedCell.row, col: selectedCell.col, value: 0,
      }))
    }
  }

  const handleUndo = () => {
    if (moves.length <= initialMoveCount) return
    prevFilledRef.current = false
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

    setMoves(prev => prev.slice(0, -1))
    setRedoMoves(prev => [lastMove, ...prev])

    if (gameId) {
      if (lastMove.type === "pencil") {
        enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/pencil-mark-history`, accessToken, "DELETE"))
      } else if (lastMove.type === "number" || lastMove.type === "batch") {
        enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "DELETE"))
      }
    }
  }

  const handleRedo = () => {
    if (redoMoves.length === 0) return
    prevFilledRef.current = false
    const moveToRedo = redoMoves[0]
    setRedoMoves(prev => prev.slice(1))
    setMoves(prev => [...prev, moveToRedo])

    if (!gameId) return

    if (moveToRedo.type === "pencil") {
      enqueueMutation(() => savePencilMarkHistory(gameId, accessToken, moveToRedo.row, moveToRedo.col, moveToRedo.value, moveToRedo.action, false))
    } else if (moveToRedo.type === "number") {
      enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "POST", {
        row: moveToRedo.row, col: moveToRedo.col, value: moveToRedo.value,
      }))
    } else if (moveToRedo.type === "batch") {
      for (const move of moveToRedo.moves) {
        enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "POST", {
          row: move.row, col: move.col, value: move.value,
        }))
      }
    }
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

  useEffect(() => {
    let allFilled = true
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (!givenCells[r][c] && grid[r][c] === 0) {
          allFilled = false
          break
        }
      }
      if (!allFilled) break
    }

    if (allFilled && !prevFilledRef.current && moves.length > 0) {
      handleCheck()
    }
    prevFilledRef.current = allFilled
  }, [grid, givenCells, moves.length, handleCheck])

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

      if (gameId) {
        for (const move of batchMoves) {
          enqueueMutation(() => sendGameMutation(`/application/v1/games/${gameId}/history`, accessToken, "POST", {
            row: move.row, col: move.col, value: move.value,
          }))
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to solve puzzle")
    }
  }, [puzzle, grid, givenCells, gameId, accessToken])

  const handleCopyTemplateId = async () => {
    if (templateId) {
      try {
        await navigator.clipboard.writeText(templateId)
        setCopyFeedback(true)
        setTimeout(() => setCopyFeedback(false), 2000)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }

  return (
    <div className="h-screen bg-background flex flex-col">
      <Header />

      <main className="flex-1 flex flex-row items-stretch px-4 py-4 pb-32 gap-4 min-h-0 overflow-hidden">
        <div className="flex-1 hidden md:flex flex-col min-h-0">
          {accessToken && gameId && (
            <GameChat gameId={gameId} accessToken={accessToken} />
          )}
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

        <div className="flex-1 flex flex-col items-center min-h-0">
          <div className="flex-1 flex items-center justify-center">
            <NumberPad
              onNumberClick={handleNumberClick}
              onDelete={handleDelete}
              onUndo={handleUndo}
              onRedo={handleRedo}
              canUndo={moves.length > initialMoveCount}
              canRedo={redoMoves.length > 0}
              pencilMode={pencilMode}
              onTogglePencil={() => setPencilMode(m => !m)}
              onCheck={handleCheck}
              onSolve={handleSolve}
            />
          </div>
          {templateId && (
            <div className="flex flex-col gap-1 items-center w-[184px] md:w-64">
              <span className="text-foreground/50 text-xs uppercase tracking-tight font-heading font-bold">Template ID</span>
              <button
                onClick={handleCopyTemplateId}
                className="w-full bg-card border-2 border-secondary/20 text-foreground/70 hover:text-foreground hover:border-secondary/40 text-[10px] font-mono px-2 py-2 rounded-xl transition-colors text-center whitespace-nowrap"
                title="Click to copy template ID"
              >
                {copyFeedback ? '✓ Copied!' : templateId}
              </button>
            </div>
          )}
        </div>
      </main>

      <BottomNav />
    </div>
  )
}
