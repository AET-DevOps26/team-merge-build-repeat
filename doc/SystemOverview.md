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

## Core Concept and Usage

### What is the main functionality?

The main functionality is an interactive Sudoku learning platform.
Users can solve Sudoku puzzles, enter numbers and notes, receive feedback on their progress, and continue unfinished games later.
The platform goes beyond a classic Sudoku game by explaining why a move is valid or invalid and by teaching the solving techniques behind the next logical steps.

### Who are the intended users?

The intended users are Sudoku players who want to improve their skills instead of only completing puzzles.
This includes beginners who need guidance with basic rules and candidates, intermediate players who want to learn common solving strategies,
and experienced players who want structured feedback on mistakes, solving time, and hint usage.
Administrators may also use the platform to manage users, monitor the system, and maintain puzzle content.

### How will you integrate GenAI meaningfully?

Generative AI will be integrated as a contextual tutor rather than as a simple answer generator.
The GenAI Service uses the current board state, user actions, mistake history, and reliable solving results from the Game Engine Service
to generate hints, explanations, and learning-oriented feedback.
This allows the system to provide different levels of help, such as a small non-spoiler hint, an explanation of a specific mistake,
or a step-by-step walkthrough of a solving technique.
The AI therefore supports learning and reasoning while the deterministic engine remains responsible for rule-based correctness.

### Describe some scenarios how your app will function?

In a typical solving scenario, a user starts a new Sudoku puzzle in the frontend.
The Application API loads a puzzle template, creates a game state, and stores the current progress in the Game Database Service.
As the user fills cells or adds pencil notes, the game state is updated so the puzzle can be resumed later.

When the user is stuck, they can ask the AI assistant for help.
The Application API sends the current board to the Game Engine Service to identify valid candidates and the next logical move.
The GenAI Service then turns this solver information into a user-friendly explanation that matches the requested hint level.

When the user makes a mistake, the platform can either warn them immediately or support delayed review depending on the selected settings.
The AI assistant can explain why the move conflicts with Sudoku rules and suggest how to recover without simply revealing the full solution.

After completing a puzzle, the user can open a review screen.
The platform summarizes solving time, mistakes, used hints, and completed techniques.
The GenAI Service can generate personalized feedback and recommend what the user should practice next.

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

### Chat Database Service

The Chat Service stores and manages the user’s active and past chat histories.

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
