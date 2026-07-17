package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.dto.HistoryRecord;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import com.sudokuai.merge_build_repeat.repository.GameHistoryRepository;
import com.sudokuai.merge_build_repeat.service.GameHistoryService;
import com.sudokuai.merge_build_repeat.service.GamePropertiesService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Collections;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class GameHistoryServiceTest {

    @Mock
    private GameHistoryRepository repository;

    @Mock
    private GamePropertiesService gamePropertiesService;

    @InjectMocks
    private GameHistoryService gameHistoryService;

    @Nested
    class SaveGameHistory {

        @Test
        void shouldSaveGameHistorySuccessfully() {
            UUID gameId = UUID.randomUUID();
            Integer row = 2;
            Integer col = 4;
            Integer value = 5;

            gameHistoryService.saveGameHistory(gameId, row, col, value);

            ArgumentCaptor<GameHistory> historyCaptor = ArgumentCaptor.forClass(GameHistory.class);
            verify(repository, times(1)).save(historyCaptor.capture());

            GameHistory savedHistory = historyCaptor.getValue();
            assertEquals(gameId, savedHistory.getGameId());
            assertEquals(row, savedHistory.getRow());
            assertEquals(col, savedHistory.getCol());
            assertEquals(value, savedHistory.getValue());
        }
    }

    @Nested
    class ValidateAndSaveMove {

        @Test
        void shouldSaveMoveAndReturnTrue() {
            UUID gameId = UUID.randomUUID();
            Integer row = 0;
            Integer col = 8;
            Integer value = 9;

            boolean result = gameHistoryService.validateAndSaveMove(gameId, row, col, value);

            assertTrue(result);
            ArgumentCaptor<GameHistory> historyCaptor = ArgumentCaptor.forClass(GameHistory.class);
            verify(repository, times(1)).save(historyCaptor.capture());

            GameHistory savedHistory = historyCaptor.getValue();
            assertEquals(gameId, savedHistory.getGameId());
            assertEquals(row, savedHistory.getRow());
            assertEquals(col, savedHistory.getCol());
            assertEquals(value, savedHistory.getValue());
            verify(gamePropertiesService).updateGameProperties(gameId, row, col, value);
        }
    }

    @Nested
    class GetHistoryRecords {

//        @Test
//        void shouldReturnMappedHistoryRecordsWhenHistoryExists() {
//            UUID gameId = UUID.randomUUID();
//
//            GameHistory history1 = new GameHistory(gameId, 1, 2, 3);
//            history1.setId(101L); // Assuming an ID field exists in GameHistory
//
//            GameHistory history2 = new GameHistory(gameId, 4, 5, 6);
//            history2.setId(102L);
//
//            List<GameHistory> mockHistoryList = List.of(history1, history2);
//            when(repository.findByGameId(gameId)).thenReturn(mockHistoryList);
//
//            List<HistoryRecord> records = gameHistoryService.getHistoryRecords(gameId);
//
//            assertNotNull(records);
//            assertEquals(2, records.size());
//
//            HistoryRecord record1 = records.get(0);
//            assertEquals(101L, record1.id()); // Matches standard record getter or h.getId()
//            assertEquals(1, record1.row());
//            assertEquals(2, record1.col());
//            assertEquals(3, record1.value());
//
//            HistoryRecord record2 = records.get(1);
//            assertEquals(102L, record2.id());
//            assertEquals(4, record2.row());
//            assertEquals(5, record2.col());
//            assertEquals(6, record2.value());
//        }

        @Test
        void shouldReturnEmptyListWhenNoHistoryExists() {
            UUID gameId = UUID.randomUUID();
            when(repository.findByGameIdOrderByCreatedAtAsc(gameId)).thenReturn(Collections.emptyList());

            List<HistoryRecord> records = gameHistoryService.getHistoryRecords(gameId);

            assertNotNull(records);
            assertTrue(records.isEmpty());
        }
    }
}
