import { useState } from "react"
import { Header, BottomNav } from "@/components/navigation"
import { SudokuGrid, NumberPad, GameStatsBar, DifficultyChip, AIHintBubble } from "@/components/game"

export default function GamePage() {
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null)
  const [grid, setGrid] = useState([
    [5, 3, 0, 1, 0, 7, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
  ])

  const handleCellClick = (row: number, col: number) => {
    setSelectedCell({ row, col })
  }

  const handleNumberClick = (num: number) => {
    if (selectedCell) {
      const newGrid = grid.map((row, rowIndex) =>
        row.map((cell, colIndex) =>
          rowIndex === selectedCell.row && colIndex === selectedCell.col ? num : cell
        )
      )
      setGrid(newGrid)
    }
  }

  const handleDelete = () => {
    if (selectedCell) {
      const newGrid = grid.map((row, rowIndex) =>
        row.map((cell, colIndex) =>
          rowIndex === selectedCell.row && colIndex === selectedCell.col ? 0 : cell
        )
      )
      setGrid(newGrid)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="flex-1 flex flex-col px-4 py-4 pb-24 max-w-lg mx-auto w-full gap-4">
        <GameStatsBar score={14250} time="12:45" />
        
        <DifficultyChip difficulty="expert" />
        
        <SudokuGrid
          grid={grid}
          selectedCell={selectedCell}
          onCellClick={handleCellClick}
        />
        
        <AIHintBubble 
          message={'"Schau dir mal die dritte Reihe an... da fehlt doch nur noch eine Zahl im letzten Block!"'}
        />
        
        <NumberPad 
          onNumberClick={handleNumberClick}
          onDelete={handleDelete}
        />
      </main>

      <BottomNav />
    </div>
  )
}
