import { cn } from "@/lib/utils"

interface SudokuGridProps {
  selectedCell?: { row: number; col: number } | null
  onCellClick?: (row: number, col: number) => void
  grid: number[][]
  givenCells: boolean[][]
  pencilMarks: number[][][]
  wrongCells?: Set<string>
  correctCells?: Set<string>
}

export function SudokuGrid({
  selectedCell,
  onCellClick,
  grid,
  givenCells,
  pencilMarks,
  wrongCells,
  correctCells,
}: SudokuGridProps) {
  const getCellBorderClasses = (row: number, col: number) => {
    const classes: string[] = []
    if ((col + 1) % 3 === 0 && col !== 8) classes.push("border-r-2 border-r-secondary")
    else if (col !== 8) classes.push("border-r border-r-border")
    if ((row + 1) % 3 === 0 && row !== 8) classes.push("border-b-2 border-b-secondary")
    else if (row !== 8) classes.push("border-b border-b-border")
    return classes.join(" ")
  }

  return (
    <div className="relative w-full h-full bg-card border-4 border-secondary p-2 shadow-[8px_8px_0px_0px_var(--color-secondary)]">
      <div className="grid grid-cols-9 grid-rows-9 gap-0 w-full h-full">
        {grid.map((row, rowIndex) =>
          row.map((cell, colIndex) => {
            const marks = pencilMarks[rowIndex][colIndex]
            const selected = selectedCell?.row === rowIndex && selectedCell?.col === colIndex
            const given = givenCells[rowIndex][colIndex]

            return (
              <button
                key={`${rowIndex}-${colIndex}`}
                onClick={() => !given && onCellClick?.(rowIndex, colIndex)}
                disabled={given}
                className={cn(
                  "grid grid-cols-3 grid-rows-3 min-h-0 min-w-0 p-0 transition-colors",
                  getCellBorderClasses(rowIndex, colIndex),
                  wrongCells?.has(`${rowIndex},${colIndex}`)
                    ? "bg-destructive"
                    : correctCells?.has(`${rowIndex},${colIndex}`)
                      ? "bg-green-500"
                      : selected
                        ? "bg-primary shadow-inner"
                        : given
                          ? "bg-muted cursor-default"
                          : "hover:bg-muted"
                )}
              >
                {cell !== 0 ? (
                  <span className={cn(
                    "col-span-3 row-span-3 flex items-center justify-center font-sans text-lg md:text-2xl lg:text-3xl font-bold",
                    wrongCells?.has(`${rowIndex},${colIndex}`) || correctCells?.has(`${rowIndex},${colIndex}`)
                      ? "text-white"
                      : selected
                        ? "text-secondary"
                        : given
                          ? "text-accent"
                          : "text-foreground"
                  )}>
                    {cell}
                  </span>
                ) : (
                  [1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
                    <span
                      key={n}
                      className={cn(
                        "flex items-center justify-center font-sans font-semibold leading-none text-[clamp(6px,1.2vw,11px)]",
                        selected ? "text-secondary/90" : "text-primary/70"
                      )}
                    >
                      {marks.includes(n) ? n : ""}
                    </span>
                  ))
                )}
              </button>
            )
          })
        )}
      </div>
    </div>
  )
}
