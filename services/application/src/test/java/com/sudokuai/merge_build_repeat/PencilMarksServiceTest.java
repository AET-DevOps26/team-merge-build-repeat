package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.model.PencilMarks;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import com.sudokuai.merge_build_repeat.service.PencilMarksService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
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
class PencilMarksServiceTest {

    @Mock
    private PencilMarksRepository pencilMarksRepository;

    @InjectMocks
    private PencilMarksService pencilMarksService;

    @Nested
    class UpdatePencilMark {

        @Test
        void shouldCreateNewPencilMarkWhenNoneExistAtCoordinates() {
            UUID gameId = UUID.randomUUID();
            int row = 3;
            int col = 5;
            int value = 7;

            when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col)).thenReturn(null);

            boolean result = pencilMarksService.updatePencilMark(gameId, row, col, value);

            assertTrue(result);
            ArgumentCaptor<PencilMarks> marksCaptor = ArgumentCaptor.forClass(PencilMarks.class);
            verify(pencilMarksRepository, times(1)).save(marksCaptor.capture());

            PencilMarks savedMarks = marksCaptor.getValue();
            assertEquals(gameId, savedMarks.getGameId());
            assertEquals(row, savedMarks.getRow());
            assertEquals(col, savedMarks.getCol());
            assertEquals("7", savedMarks.getMarks());
        }

        @Test
        void shouldAppendToExistingPencilMarkWhenMarkValueIsNew() {
            UUID gameId = UUID.randomUUID();
            int row = 0;
            int col = 0;
            int value = 4;

            PencilMarks existingMarks = new PencilMarks();
            existingMarks.setGameId(gameId);
            existingMarks.setRow(row);
            existingMarks.setCol(col);
            existingMarks.setMarks("123");

            when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col)).thenReturn(existingMarks);

            boolean result = pencilMarksService.updatePencilMark(gameId, row, col, value);

            assertTrue(result);
            verify(pencilMarksRepository, times(1)).save(existingMarks);
            assertEquals("1234", existingMarks.getMarks());
        }

        @Test
        void shouldReturnFalseAndNotSaveWhenMarkValueAlreadyExists() {
            UUID gameId = UUID.randomUUID();
            int row = 1;
            int col = 1;
            int value = 5;

            PencilMarks existingMarks = new PencilMarks();
            existingMarks.setGameId(gameId);
            existingMarks.setRow(row);
            existingMarks.setCol(col);
            existingMarks.setMarks("258");

            when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, col)).thenReturn(existingMarks);

            boolean result = pencilMarksService.updatePencilMark(gameId, row, col, value);

            assertFalse(result);
            verify(pencilMarksRepository, never()).save(any(PencilMarks.class));
            assertEquals("258", existingMarks.getMarks()); // Remains unchanged
        }

        @ParameterizedTest
        @CsvSource({
                "-1, 0, 5",
                "9, 0, 5",
                "0, -1, 5",
                "0, 9, 5",
                "0, 0, 0",
                "0, 0, 10"
        })
        void shouldReturnFalseWhenInputsAreOutOfBounds(int row, int col, int value) {
            UUID gameId = UUID.randomUUID();

            boolean result = pencilMarksService.updatePencilMark(gameId, row, col, value);

            assertFalse(result);
            verifyNoInteractions(pencilMarksRepository);
        }
    }

    @Nested
    class DeletePencilMark {

        @Test
        void shouldRemoveValueFromExistingPencilMarks() {
            UUID gameId = UUID.randomUUID();
            int row = 4;
            int column = 4;
            int valueToDelete = 3;

            PencilMarks existingMarks = new PencilMarks();
            existingMarks.setGameId(gameId);
            existingMarks.setRow(row);
            existingMarks.setCol(column);
            existingMarks.setMarks("135");

            when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, column)).thenReturn(existingMarks);

            pencilMarksService.deletePencilMark(gameId, row, column, valueToDelete);

            verify(pencilMarksRepository, times(1)).save(existingMarks);
            assertEquals("15", existingMarks.getMarks());
        }

        @Test
        void shouldDoNothingWhenNoPencilMarksExistAtCoordinates() {
            UUID gameId = UUID.randomUUID();
            int row = 2;
            int column = 2;

            when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, row, column)).thenReturn(null);

            pencilMarksService.deletePencilMark(gameId, row, column, 9);

            verify(pencilMarksRepository, never()).save(any(PencilMarks.class));
        }
    }

    @Nested
    class GetPencilMarks {

        @Test
        void shouldBuildAndPopulate9x9GridOfListsSuccessfully() {
            UUID gameId = UUID.randomUUID();

            PencilMarks mark1 = new PencilMarks();
            mark1.setGameId(gameId);
            mark1.setRow(0);
            mark1.setCol(2);
            mark1.setMarks("15");

            PencilMarks mark2 = new PencilMarks();
            mark2.setGameId(gameId);
            mark2.setRow(8);
            mark2.setCol(8);
            mark2.setMarks("9");

            // Element belonging to a different gameId to test structural filtering condition
            PencilMarks mixedMark = new PencilMarks();
            mixedMark.setGameId(UUID.randomUUID());
            mixedMark.setRow(4);
            mixedMark.setCol(4);
            mixedMark.setMarks("7");

            when(pencilMarksRepository.findByGameId(gameId)).thenReturn(List.of(mark1, mark2, mixedMark));

            List<List<List<Integer>>> gridResult = pencilMarksService.getPencilMarks(gameId);

            assertNotNull(gridResult);
            assertEquals(9, gridResult.size());
            assertEquals(9, gridResult.get(0).size());

            // Check populated marks matching the gameId
            assertEquals(List.of(1, 5), gridResult.get(0).get(2));
            assertEquals(List.of(9), gridResult.get(8).get(8));

            // Check mismatched gameId wasn't mapped
            assertTrue(gridResult.get(4).get(4).isEmpty());

            // Check unpopulated cell yields an empty list container
            assertTrue(gridResult.get(0).get(0).isEmpty());
        }

        @Test
        void shouldReturnCompletelyEmpty9x9GridWhenNoMarksFound() {
            UUID gameId = UUID.randomUUID();
            when(pencilMarksRepository.findByGameId(gameId)).thenReturn(Collections.emptyList());

            List<List<List<Integer>>> gridResult = pencilMarksService.getPencilMarks(gameId);

            assertNotNull(gridResult);
            assertEquals(9, gridResult.size());
            for (int i = 0; i < 9; i++) {
                assertEquals(9, gridResult.get(i).size());
                for (int j = 0; j < 9; j++) {
                    assertTrue(gridResult.get(i).get(j).isEmpty(), "Cell coordinates must initialize completely empty");
                }
            }
        }
    }
}
