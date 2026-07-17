package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.PencilMarkHistoryEntry;
import com.sudokuai.merge_build_repeat.model.PencilMarkHistory;
import com.sudokuai.merge_build_repeat.model.PencilMarks;
import com.sudokuai.merge_build_repeat.repository.PencilMarkHistoryRepository;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class PencilMarksService {
    PencilMarksRepository pencilMarksRepository;
    PencilMarkHistoryRepository pencilMarkHistoryRepository;

    /**
     * Stores only candidates explicitly removed by the player. Candidates that
     * remain possible are calculated from the current board when requested.
     */
    @Transactional
    public boolean updatePencilMark(UUID gameId, int row, int col, int value) {
        if (!isValidPosition(row, col, value)) {
            return false;
        }

        PencilMarks excludedMarks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col);
        if (excludedMarks == null || !excludedMarks.getMarks().contains(String.valueOf(value))) {
            return false;
        }

        String remainingExclusions = excludedMarks.getMarks().replace(String.valueOf(value), "");
        if (remainingExclusions.isEmpty()) {
            pencilMarksRepository.delete(excludedMarks);
        } else {
            excludedMarks.setMarks(remainingExclusions);
            pencilMarksRepository.save(excludedMarks);
        }
        return true;
    }

    @Transactional
    public boolean deletePencilMark(UUID gameId, int row, int col, int value) {
        if (!isValidPosition(row, col, value)) {
            return false;
        }

        String markValue = String.valueOf(value);
        PencilMarks excludedMarks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col);
        if (excludedMarks == null) {
            excludedMarks = new PencilMarks();
            excludedMarks.setGameId(gameId);
            excludedMarks.setRow(row);
            excludedMarks.setCol(col);
            excludedMarks.setMarks(markValue);
        } else if (excludedMarks.getMarks().contains(markValue)) {
            return false;
        } else {
            excludedMarks.setMarks(excludedMarks.getMarks() + markValue);
        }
        pencilMarksRepository.save(excludedMarks);
        return true;
    }

    @Transactional
    public void saveToHistory(UUID gameId, int row, int col, int value, String action, boolean initial) {
        if ("ADD".equals(action)) {
            updatePencilMark(gameId, row, col, value);
        } else if ("REMOVE".equals(action)) {
            deletePencilMark(gameId, row, col, value);
        } else {
            return;
        }
        pencilMarkHistoryRepository.save(new PencilMarkHistory(gameId, row, col, value, action, initial));
    }

    @Transactional
    public void undoLastPencilMarkHistory(UUID gameId) {
        List<PencilMarkHistory> history = pencilMarkHistoryRepository.findByGameIdOrderByCreatedAtAsc(gameId);
        PencilMarkHistory last = null;
        for (PencilMarkHistory entry : history) {
            if (!entry.isInitial()) {
                last = entry;
            }
        }
        if (last == null) {
            return;
        }
        if ("ADD".equals(last.getAction())) {
            deletePencilMark(gameId, last.getRow(), last.getCol(), last.getValue());
        } else {
            updatePencilMark(gameId, last.getRow(), last.getCol(), last.getValue());
        }
        pencilMarkHistoryRepository.delete(last);
    }

    public List<PencilMarkHistoryEntry> getPencilMarkHistory(UUID gameId) {
        return pencilMarkHistoryRepository.findByGameIdOrderByCreatedAtAsc(gameId).stream()
                .map(entry -> new PencilMarkHistoryEntry(entry.getRow(), entry.getCol(), entry.getValue(), entry.getAction(), entry.isInitial(), entry.getCreatedAt()))
                .toList();
    }

    public List<List<List<Integer>>> getPencilMarks(UUID gameId, List<List<Integer>> board) {
        List<List<List<Integer>>> candidates = calculateCandidates(board);
        for (PencilMarks excludedMarks : pencilMarksRepository.findByGameId(gameId)) {
            if (!gameId.equals(excludedMarks.getGameId())) {
                continue;
            }
            List<Integer> cellCandidates = candidates.get(excludedMarks.getRow()).get(excludedMarks.getCol());
            for (char value : excludedMarks.getMarks().toCharArray()) {
                cellCandidates.remove(Integer.valueOf(Character.getNumericValue(value)));
            }
        }
        return candidates;
    }

    private List<List<List<Integer>>> calculateCandidates(List<List<Integer>> board) {
        validateBoard(board);
        List<List<List<Integer>>> candidates = new ArrayList<>(9);
        for (int row = 0; row < 9; row++) {
            List<List<Integer>> candidateRow = new ArrayList<>(9);
            for (int col = 0; col < 9; col++) {
                List<Integer> cellCandidates = new ArrayList<>();
                if (board.get(row).get(col) == 0) {
                    for (int value = 1; value <= 9; value++) {
                        if (isCandidateAllowed(board, row, col, value)) {
                            cellCandidates.add(value);
                        }
                    }
                }
                candidateRow.add(cellCandidates);
            }
            candidates.add(candidateRow);
        }
        return candidates;
    }

    private boolean isCandidateAllowed(List<List<Integer>> board, int row, int col, int value) {
        for (int index = 0; index < 9; index++) {
            if (board.get(row).get(index) == value || board.get(index).get(col) == value) {
                return false;
            }
        }
        int boxRow = row / 3 * 3;
        int boxCol = col / 3 * 3;
        for (int currentRow = boxRow; currentRow < boxRow + 3; currentRow++) {
            for (int currentCol = boxCol; currentCol < boxCol + 3; currentCol++) {
                if (board.get(currentRow).get(currentCol) == value) {
                    return false;
                }
            }
        }
        return true;
    }

    private void validateBoard(List<List<Integer>> board) {
        if (board == null || board.size() != 9) {
            throw new IllegalArgumentException("A Sudoku board must have 9 rows");
        }
        for (List<Integer> row : board) {
            if (row == null || row.size() != 9) {
                throw new IllegalArgumentException("A Sudoku board must have 9 columns per row");
            }
            for (Integer value : row) {
                if (value == null || value < 0 || value > 9) {
                    throw new IllegalArgumentException("Sudoku values must be between 0 and 9");
                }
            }
        }
    }

    private boolean isValidPosition(int row, int col, int value) {
        return row >= 0 && row < 9 && col >= 0 && col < 9 && value >= 1 && value <= 9;
    }
}
