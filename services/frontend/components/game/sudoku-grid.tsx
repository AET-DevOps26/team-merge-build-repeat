import { cn } from "@/lib/utils"

// Sample Sudoku grid data - in a real app this would come from game state
const initialGrid = [
  [5, 3, 0, 1, 0, 7, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

// Track which cells are pre-filled (given) vs user-entered
const givenCells = initialGrid.map(row => row.map(cell => cell !== 0))

interface SudokuGridProps {
  selectedCell?: { row: number; col: number } | null
  onCellClick?: (row: number, col: number) => void
  grid?: number[][]
}

export function SudokuGrid({ 
  selectedCell, 
  onCellClick,
  grid = initialGrid 
}: SudokuGridProps) {
  const getCellBorderClasses = (row: number, col: number) => {
    const classes: string[] = []
    
    // Right borders for 3x3 blocks
    if ((col + 1) % 3 === 0 && col !== 8) {
      classes.push("border-r-2 border-r-secondary")
    } else if (col !== 8) {
      classes.push("border-r border-r-border")
    }
    
    // Bottom borders for 3x3 blocks
    if ((row + 1) % 3 === 0 && row !== 8) {
      classes.push("border-b-2 border-b-secondary")
    } else if (row !== 8) {
      classes.push("border-b border-b-border")
    }
    
    return classes.join(" ")
  }

  const isSelected = (row: number, col: number) => 
    selectedCell?.row === row && selectedCell?.col === col

  const isGiven = (row: number, col: number) => givenCells[row][col]

  return (
    <div className="relative w-full aspect-square bg-card border-4 border-secondary p-1 shadow-[8px_8px_0px_0px_var(--color-secondary)]">
      <div className="grid grid-cols-9 grid-rows-9 gap-0 w-full h-full">
        {grid.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <button
              key={`${rowIndex}-${colIndex}`}
              onClick={() => onCellClick?.(rowIndex, colIndex)}
              className={cn(
                "flex items-center justify-center font-sans text-xl sm:text-2xl md:text-3xl font-bold transition-colors",
                getCellBorderClasses(rowIndex, colIndex),
                isSelected(rowIndex, colIndex)
                  ? "bg-primary text-secondary shadow-inner"
                  : isGiven(rowIndex, colIndex)
                    ? "bg-muted text-accent"
                    : "text-foreground hover:bg-muted"
              )}
            >
              {cell !== 0 ? cell : ""}
            </button>
          ))
        )}
      </div>
    </div>
  )
}
