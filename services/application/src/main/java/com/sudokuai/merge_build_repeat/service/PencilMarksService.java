package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.model.PencilMarks;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
@AllArgsConstructor
public class PencilMarksService {
    PencilMarksRepository pencilMarksRepository;


    public boolean updatePencilMark(UUID gameId, int row, int col, int value) {
        PencilMarks marks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col);
        if (marks == null) {
            marks = new PencilMarks();
            marks.setGameId(gameId);
            marks.setRow(row);
            marks.setCol(col);
            marks.setMarks(String.valueOf(value));
        } else {
            String existingMarks = marks.getMarks();
            if (!existingMarks.contains(String.valueOf(value))) {
                existingMarks += String.valueOf(value);
            } else {
                return false;
            }
            marks.setMarks(existingMarks);
        }
        pencilMarksRepository.save(marks);
        return true;
    }

    public void deletePencilMark(UUID gameId, int row, int column, int value) {
        PencilMarks marks = pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, column);
        if (marks != null) {
            String existingMarks = marks.getMarks();
            existingMarks = existingMarks.replace(String.valueOf(value), "");
            marks.setMarks(existingMarks);
            pencilMarksRepository.save(marks);
        }
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
