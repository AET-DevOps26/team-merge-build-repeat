package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.PencilMarkHistoryEntry;
import com.sudokuai.merge_build_repeat.model.PencilMarkHistory;
import com.sudokuai.merge_build_repeat.model.PencilMarks;
import com.sudokuai.merge_build_repeat.repository.PencilMarkHistoryRepository;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class PencilMarksService {
    PencilMarksRepository pencilMarksRepository;
    PencilMarkHistoryRepository pencilMarkHistoryRepository;


    @Transactional
    public boolean updatePencilMark(UUID gameId, int row, int col, int value) {
        if (row < 0 || row > 8 || col < 0 || col > 8 || value < 1 || value > 9) {
            return false;
        }

        String markValue = String.valueOf(value);
        PencilMarks marks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col);
        if (marks == null) {
            marks = new PencilMarks();
            marks.setGameId(gameId);
            marks.setRow(row);
            marks.setCol(col);
            marks.setMarks(markValue);
        } else {
            String existingMarks = marks.getMarks();
            if (!existingMarks.contains(markValue)) {
                existingMarks += markValue;
            } else {
                return false;
            }
            marks.setMarks(existingMarks);
        }
        pencilMarksRepository.save(marks);
        return true;
    }

    @Transactional
    public boolean deletePencilMark(UUID gameId, int row, int column, int value) {
        if (row < 0 || row > 8 || column < 0 || column > 8 || value < 1 || value > 9) {
            return false;
        }

        PencilMarks marks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, column);
        if (marks == null || !marks.getMarks().contains(String.valueOf(value))) {
            return false;
        }

        marks.setMarks(marks.getMarks().replace(String.valueOf(value), ""));
        pencilMarksRepository.save(marks);
        return true;
    }

    @Transactional
    public void saveToHistory(UUID gameId, int row, int col, int value, String action, boolean initial) {
        boolean changed;
        if ("ADD".equals(action)) {
            changed = updatePencilMark(gameId, row, col, value);
        } else if ("REMOVE".equals(action)) {
            changed = deletePencilMark(gameId, row, col, value);
        } else {
            return;
        }

        if (changed) {
            pencilMarkHistoryRepository.save(new PencilMarkHistory(gameId, row, col, value, action, initial));
        }
    }

    @Transactional
    public void undoLastPencilMarkHistory(UUID gameId) {
        List<PencilMarkHistory> history = pencilMarkHistoryRepository.findByGameIdOrderByCreatedAtAsc(gameId);
        PencilMarkHistory last = null;
        for (PencilMarkHistory h : history) {
            if (!h.isInitial()) last = h;
        }
        if (last == null) return;
        if ("ADD".equals(last.getAction())) {
            deletePencilMark(gameId, last.getRow(), last.getCol(), last.getValue());
        } else {
            updatePencilMark(gameId, last.getRow(), last.getCol(), last.getValue());
        }
        pencilMarkHistoryRepository.delete(last);
    }

    public List<PencilMarkHistoryEntry> getPencilMarkHistory(UUID gameId) {
        return pencilMarkHistoryRepository.findByGameIdOrderByCreatedAtAsc(gameId).stream()
                .map(h -> new PencilMarkHistoryEntry(h.getRow(), h.getCol(), h.getValue(), h.getAction(), h.isInitial(), h.getCreatedAt()))
                .toList();
    }

    public List<List<List<Integer>>> getPencilMarks(UUID gameId) {
        List<PencilMarks> marksList = pencilMarksRepository.findByGameId(gameId);
        List<List<List<Integer>>> pencilMarks = new java.util.ArrayList<>(9);
        for (int i = 0; i < 9; i++) {
            List<List<Integer>> rowMarks = new java.util.ArrayList<>(9);
            for (int j = 0; j < 9; j++) {
                rowMarks.add(new java.util.ArrayList<>());
            }
            pencilMarks.add(rowMarks);
        }

        for (PencilMarks marks : marksList) {
            if (marks.getGameId().equals(gameId)) {
                int row = marks.getRow();
                int col = marks.getCol();
                String markString = marks.getMarks();
                List<Integer> markValues = new java.util.ArrayList<>();
                for (char c : markString.toCharArray()) {
                    markValues.add(Character.getNumericValue(c));
                }
                pencilMarks.get(row).set(col, markValues);
            }
        }
        return pencilMarks;
    }
}
