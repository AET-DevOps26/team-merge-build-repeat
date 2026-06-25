package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.HistoryRecord;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import com.sudokuai.merge_build_repeat.repository.GameHistoryRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class GameHistoryService {

    GameHistoryRepository repository;

    public void saveGameHistory(Long gameId, Integer row, Integer col, Integer value) {
        repository.save(new GameHistory(gameId, row, col, value));
    }

    public boolean validateAndSaveMove(Long gameId, Integer row, Integer col, Integer value) {
        return false;
    }

    public List<HistoryRecord> getHistoryRecords(Long gameId) {
        return null;
    }
}
