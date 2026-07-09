import os

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sudoku_solver import generate_sudoku, get_solution


def normalize_root_path(value: str) -> str:
    root_path = value.strip()
    if root_path == "/":
        return ""
    return root_path.rstrip("/")


class SudokuRequest(BaseModel):
    sudoku: list[list[int]]


app = FastAPI(
    title="Game Engine Service",
    version=os.getenv("APP_VERSION", "0.1.0"),
    description="FastAPI service for game engine",
    root_path=normalize_root_path(os.getenv("GAME_ENGINE_ROOT_PATH", "")),
)

Instrumentator().instrument(app).expose(app)


@app.get("/actuator/health", tags=["actuator"])
async def health():
    """Health check endpoint"""
    return {"status": "UP"}


@app.get("/actuator/info", tags=["actuator"])
async def info():
    """Build info endpoint"""
    return {
        "build": {
            "version": os.getenv("APP_VERSION", "0.1.0"),
            "commit": os.getenv("GIT_COMMIT", "unknown"),
        }
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse({"message": "Game Engine Service is running"})


@app.get("/sudoku")
async def get_sudoku():
    """Get a random Sudoku puzzle"""
    sudoku = generate_sudoku()
    return JSONResponse({"sudoku": sudoku})


@app.post("/solution")
async def solution(request: SudokuRequest):
    """Get the solution for a Sudoku puzzle"""
    solved = get_solution(request.sudoku)
    return JSONResponse({"sudoku": solved})
