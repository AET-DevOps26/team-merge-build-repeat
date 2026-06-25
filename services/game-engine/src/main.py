from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sudoku_solver import generate_sudoku

app = FastAPI(
    title="Game Engine Service",
    version="0.1.0",
    description="FastAPI service for game engine"
)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy"})


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse({"message": "Game Engine Service is running"})


@app.get("/sudoku")
async def get_sudoku():
    """Get a random Sudoku puzzle"""
    sudoku = generate_sudoku()
    return JSONResponse({"sudoku": sudoku})
