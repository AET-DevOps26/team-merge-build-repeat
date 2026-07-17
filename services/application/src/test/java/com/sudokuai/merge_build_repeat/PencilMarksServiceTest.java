package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.model.PencilMarks;
import com.sudokuai.merge_build_repeat.repository.PencilMarkHistoryRepository;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import com.sudokuai.merge_build_repeat.service.PencilMarksService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class PencilMarksServiceTest {

    @Mock
    private PencilMarksRepository pencilMarksRepository;

    @Mock
    private PencilMarkHistoryRepository pencilMarkHistoryRepository;

    @InjectMocks
    private PencilMarksService pencilMarksService;

    @Test
    void deletePencilMarkShouldStoreOnlyTheRemovedCandidate() {
        UUID gameId = UUID.randomUUID();
        when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, 0, 2)).thenReturn(null);

        assertTrue(pencilMarksService.deletePencilMark(gameId, 0, 2, 2));

        ArgumentCaptor<PencilMarks> captor = ArgumentCaptor.forClass(PencilMarks.class);
        verify(pencilMarksRepository).save(captor.capture());
        assertEquals("2", captor.getValue().getMarks());
    }

    @Test
    void updatePencilMarkShouldRemoveAnExclusionWhenTheCandidateIsRestored() {
        UUID gameId = UUID.randomUUID();
        PencilMarks excludedMarks = new PencilMarks();
        excludedMarks.setGameId(gameId);
        excludedMarks.setRow(0);
        excludedMarks.setCol(2);
        excludedMarks.setMarks("2");
        when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, 0, 2)).thenReturn(excludedMarks);

        assertTrue(pencilMarksService.updatePencilMark(gameId, 0, 2, 2));

        verify(pencilMarksRepository).delete(excludedMarks);
    }

    @Test
    void getPencilMarksShouldCalculateCandidatesAndApplyStoredExclusions() {
        UUID gameId = UUID.randomUUID();
        PencilMarks excludedMarks = new PencilMarks();
        excludedMarks.setGameId(gameId);
        excludedMarks.setRow(0);
        excludedMarks.setCol(2);
        excludedMarks.setMarks("2");
        when(pencilMarksRepository.findByGameId(gameId)).thenReturn(List.of(excludedMarks));

        List<List<List<Integer>>> candidates = pencilMarksService.getPencilMarks(gameId, board());

        assertEquals(List.of(1, 4), candidates.get(0).get(2));
        assertTrue(candidates.get(0).get(0).isEmpty());
    }

    @Test
    void updatePencilMarkShouldRejectCandidatesThatAreNotExcluded() {
        UUID gameId = UUID.randomUUID();
        when(pencilMarksRepository.findByGameIdAndRowAndCol(gameId, 0, 2)).thenReturn(null);

        assertFalse(pencilMarksService.updatePencilMark(gameId, 0, 2, 2));
        verify(pencilMarksRepository, never()).save(any());
    }

    private List<List<Integer>> board() {
        return List.of(
                List.of(5, 3, 0, 0, 7, 0, 0, 0, 0),
                List.of(6, 0, 0, 1, 9, 5, 0, 0, 0),
                List.of(0, 9, 8, 0, 0, 0, 0, 6, 0),
                List.of(8, 0, 0, 0, 6, 0, 0, 0, 3),
                List.of(4, 0, 0, 8, 0, 3, 0, 0, 1),
                List.of(7, 0, 0, 0, 2, 0, 0, 0, 6),
                List.of(0, 6, 0, 0, 0, 0, 2, 8, 0),
                List.of(0, 0, 0, 4, 1, 9, 0, 0, 5),
                List.of(0, 0, 0, 0, 8, 0, 0, 7, 9));
    }
}
