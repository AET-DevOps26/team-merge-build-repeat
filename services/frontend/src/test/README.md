# Frontend Tests

This directory contains unit and integration tests for the Paulana Zudokyu frontend application.

## Running Tests

```bash
# Run all tests
npm run test

# Watch mode
npm run test -- --watch

# UI mode (interactive test explorer)
npm run test:ui

# Coverage report
npm run test -- --coverage
```

## Test Structure

### Utility Tests
- **sudoku-utils.test.ts** - UUID formatting and validation utilities used in HomePage
- **candidate-marks.test.ts** - Sudoku candidate mark computation algorithm
- **grid-state.test.ts** - Game state management and move handling
- **api-mocks.test.ts** - API fetch patterns and error handling

### Component Tests
- **game-context.test.tsx** - GameProvider context behavior and localStorage persistence
- **home-page.test.tsx** - HomePage component rendering and user interactions
- **app-routing.test.tsx** - Route structure and navigation

## What's Tested

### Game Logic
- ✓ Candidate mark calculation (respecting sudoku constraints)
- ✓ Grid state management (moves, undo/redo)
- ✓ Batch move processing
- ✓ Pencil mark operations (add/remove)

### UI & Forms
- ✓ UUID validation and formatting
- ✓ Difficulty button rendering
- ✓ Template ID input handling
- ✓ Error message display
- ✓ Loading states

### State Management
- ✓ GameProvider localStorage persistence
- ✓ User context switching
- ✓ Active game tracking

### Routing
- ✓ Protected route structure
- ✓ Login page accessibility
- ✓ Game page navigation

## Coverage Goals

These tests focus on:
1. Core game logic (sudoku rules, move history)
2. Data validation (UUID format, user input)
3. State persistence (localStorage, context)
4. API communication patterns

Component rendering tests are minimal since the UI is primarily validated through manual testing. Integration tests focus on how components interact with their context and manage state.

## Adding New Tests

When adding new features:
1. Add utility function tests alongside the implementation
2. Mock external dependencies (auth, navigation, API calls)
3. Focus on testable logic over implementation details
4. Use the existing patterns for consistency
