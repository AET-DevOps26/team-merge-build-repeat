# System Overview

## Project Statment

Sudoku learners often struggle to understand why a specific move is correct or incorrect.
Existing Sudoku platforms usually provide simple hints or mark errors,
but they often fail to explain the reasoning behind a move or teach the solving techniques needed to improve over time.

This project addresses that problem by developing a Sudoku platform with integrated Generative AI.
The platform supports users while solving Sudoku puzzles by providing contextual help,
explaining mistakes, and teaching relevant solving strategies.
Instead of only giving the next answer, the system aims to guide users through the logical reasoning process,
helping them learn Sudoku techniques and improve their problem-solving skills.

## Components

### Authentication Service

The Authentication Service manages user accounts through Supabase Auth.
It handles registration, login, logout, and account recovery.
After login, it provides secure authentication tokens so the frontend and backend can identify the current user.

It also helps ensure that users can only access their own data and supports roles such as regular users, premium users, and administrators.

- Supabase Auth (JWT, Postgress)

### Application API Service

The Application API Service is the central stateless entry point for the frontend.
It exposes the main REST API of the Sudoku platform and coordinates requests between the other backend services.

The service forwards user-related requests to the Authentication Service, retrieves and updates game data through the Game Database Service,
requests solving information from the Engine Service, and communicates with the GenAI Service when explanations or hints are needed.

The game templates are stored staticly in this service.

- Spring Boot REST API
- Java 21

### Game Engine Service

The Engine Service is a stateless service that provides the algorithmic Sudoku-solving logic for the platform.
It receives a partially completed Sudoku board and analyzes the current game state to calculate valid next steps.

The service can identify possible candidates for empty cells, detect logical solving opportunities,
and suggest the next moves based on Sudoku rules and solving techniques.

- Sprint Boot REST API
- Java 21

### Game Database Service

The Game State Service stores and manages the user’s active and past Sudoku games.
It keeps track of the current board state, user entries, notes, and completion status.
This allows users to resume unfinished games and review previously completed puzzles.

- Spring Boot REST API
- Java 21
- Postgress Database

### Frontend

The Frontend provides the user interface of the Sudoku platform and connects the user with the different backend services.
It allows users to start new games, continue active games, review past games, access profile statistics, and manage settings.

The main game screen displays the Sudoku board, editing tools such as pencil notes, warnings, and the integrated AI assistant.
Through the AI chat, users can request hints, ask questions, receive explanations, and get support while solving a puzzle.

After a game is completed, the frontend provides a game review screen that summarizes mistakes, solving time, used hints,
and AI-generated feedback.
This review can include lessons learned and recommendations for further practice.

- React (Type Script)

### GenAI Service

The GenAI Service provides the intelligent tutoring and explanation features of the Sudoku platform.
It receives the current board state, user actions, mistakes, and solver results from other services
and generates context-aware hints, explanations, and coaching responses.

The service supports different levels of assistance, from small non-spoiler hints to step-by-step explanations of the next logical move.
It can explain Sudoku techniques, analyze mistakes, guide users through delayed error handling and recovery workflows,
and adapt its response style to the user’s skill level.

The GenAI Service does not solve the Sudoku purely on its own.
Instead, it uses results from the Engine Service as a reliable logical foundation and transforms them into understandable,
user-friendly explanations.

- LangChain
- Python 3.12
- FastAPI

### Prometheus

Prometheus is used to monitor the backend services of the Sudoku platform.
It collects metrics such as request counts, response times, error rates, memory usage, and service availability.
These metrics help detect performance issues, service failures, and unusual system behavior.

### Grafana

Grafana is used to visualize monitoring data from the Sudoku platform.
It displays metrics collected by Prometheus in dashboards, charts, and tables.
This helps the development team observe service health, request latency, error rates, resource usage, and GenAI usage.
