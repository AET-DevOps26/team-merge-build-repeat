package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.HistoryRecord;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import com.sudokuai.merge_build_repeat.repository.GameHistoryRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class GameHistoryService {

    GameHistoryRepository repository;
    GamePropertiesService gamePropertiesService;

    public void saveGameHistory(UUID gameId, Integer row, Integer col, Integer value) {
        repository.save(new GameHistory(gameId, row, col, value));
    }

    public boolean validateAndSaveMove(UUID gameId, Integer row, Integer col, Integer value) {
        if (gameId == null || row == null || col == null || value == null) {
            return false;
        }
        if (row < 0 || row > 8 || col < 0 || col > 8 || value < 0 || value > 9) {
            return false;
        }

        repository.save(new GameHistory(gameId, row, col, value));
        return true;
    }

    public List<HistoryRecord> getHistoryRecords(UUID gameId) {
         List<GameHistory> history = repository.findByGameIdOrderByCreatedAtAsc(gameId);

//         if (history == null || history.isEmpty()) {
//         throw new RuntimeException("No history found for gameId: " + gameId);
//         }

         return history.stream()
         .map(h -> new HistoryRecord(h.getId(), h.getRow(), h.getCol(), h.getValue(), h.getCreatedAt()))
         .toList();
    }

    public void undoLastMove(UUID gameId) {
        List<GameHistory> history = repository.findByGameIdOrderByCreatedAtAsc(gameId);
        if (!history.isEmpty()) {
            repository.delete(history.get(history.size() - 1));
            gamePropertiesService.recalculateStateFromHistory(gameId);
        }
    }
}
