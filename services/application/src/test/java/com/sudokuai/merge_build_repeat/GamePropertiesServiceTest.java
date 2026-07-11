package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import com.sudokuai.merge_build_repeat.service.GamePropertiesService;
import com.sudokuai.merge_build_repeat.service.MapperService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class GamePropertiesServiceTest {

    @Mock
    private GamePropertiesRepository repository;

    @Mock
    private GameTemplateRepository templateRepository;

    @Mock
    private MapperService mapperService;

    @InjectMocks
    private GamePropertiesService gamePropertiesService;

    @Nested
    class SaveNewGameProperties {

        @Test
        void shouldSaveAndReturnPropertiesId() {
            UUID gameId = UUID.randomUUID();
            UUID templateId = UUID.randomUUID();
            String currentState = "000000000";

            // Assuming GameProperties generates an ID or you want to verify it returns whatever properties.getId() evaluates to.
            UUID resultId = gamePropertiesService.saveNewGameProperties(gameId, templateId, currentState);

            ArgumentCaptor<GameProperties> propertiesCaptor = ArgumentCaptor.forClass(GameProperties.class);
            verify(repository, times(1)).save(propertiesCaptor.capture());

            GameProperties savedProperties = propertiesCaptor.getValue();
            assertEquals(gameId, savedProperties.getId()); // or wherever the constructor maps gameId
            assertEquals(templateId, savedProperties.getTemplateId());
            assertEquals(currentState, savedProperties.getCurrentState());
            assertEquals(savedProperties.getId(), resultId);
        }
    }

    @Nested
    class GetGamePropertiesByGameId {

        @Test
        void shouldReturnPropertiesWhenFound() {
            UUID gameId = UUID.randomUUID();
            GameProperties properties = new GameProperties(gameId, UUID.randomUUID(), "state");
            when(repository.findById(gameId)).thenReturn(Optional.of(properties));

            GameProperties result = gamePropertiesService.getGamePropertiesByGameId(gameId);

            assertNotNull(result);
            assertEquals(properties, result);
        }

        @Test
        void shouldReturnNullWhenNotFound() {
            UUID gameId = UUID.randomUUID();
            when(repository.findById(gameId)).thenReturn(Optional.empty());

            GameProperties result = gamePropertiesService.getGamePropertiesByGameId(gameId);

            assertNull(result);
        }
    }

    @Nested
    class GetCurrentState {

        @Test
        void shouldReturnMappedListWhenPropertiesExist() {
            UUID gameId = UUID.randomUUID();
            String stateStr = "530070000...";
            GameProperties properties = new GameProperties(gameId, UUID.randomUUID(), stateStr);
            List<List<Integer>> expectedGrid = List.of(List.of(5, 3, 0));

            when(repository.findById(gameId)).thenReturn(Optional.of(properties));
            when(mapperService.mapToList(stateStr)).thenReturn(expectedGrid);

            List<List<Integer>> result = gamePropertiesService.getCurrentState(gameId);

            assertEquals(expectedGrid, result);
        }

        @Test
        void shouldReturnNullWhenPropertiesNotFound() {
            UUID gameId = UUID.randomUUID();
            when(repository.findById(gameId)).thenReturn(Optional.empty());

            List<List<Integer>> result = gamePropertiesService.getCurrentState(gameId);

            assertNull(result);
            verifyNoInteractions(mapperService);
        }
    }

    @Nested
    class GetSolution {

        @Test
        void shouldReturnMappedSolutionWhenPropertiesAndTemplateExist() {
            UUID gameId = UUID.randomUUID();
            UUID templateId = UUID.randomUUID();
            String solutionStr = "534678912...";

            GameProperties properties = new GameProperties(gameId, templateId, "current");
            GameTemplate template = new GameTemplate();
            template.setSolutionData(solutionStr);
            List<List<Integer>> expectedGrid = List.of(List.of(5, 3, 4));

            when(repository.findById(gameId)).thenReturn(Optional.of(properties));
            when(templateRepository.findById(templateId)).thenReturn(Optional.of(template));
            when(mapperService.mapToList(solutionStr)).thenReturn(expectedGrid);

            List<List<Integer>> result = gamePropertiesService.getSolution(gameId);

            assertEquals(expectedGrid, result);
        }

        @Test
        void shouldReturnNullWhenPropertiesNotFound() {
            UUID gameId = UUID.randomUUID();
            when(repository.findById(gameId)).thenReturn(Optional.empty());

            List<List<Integer>> result = gamePropertiesService.getSolution(gameId);

            assertNull(result);
            verifyNoInteractions(templateRepository, mapperService);
        }
    }

    @Nested
    class GetTemplateData {

        @Test
        void shouldReturnMappedTemplateDataWhenPropertiesAndTemplateExist() {
            UUID gameId = UUID.randomUUID();
            UUID templateId = UUID.randomUUID();
            String templateDataStr = "004070010...";

            GameProperties properties = new GameProperties(gameId, templateId, "current");
            GameTemplate template = new GameTemplate();
            template.setTemplateData(templateDataStr);
            List<List<Integer>> expectedGrid = List.of(List.of(0, 0, 4));

            when(repository.findById(gameId)).thenReturn(Optional.of(properties));
            when(templateRepository.findById(templateId)).thenReturn(Optional.of(template));
            when(mapperService.mapToList(templateDataStr)).thenReturn(expectedGrid);

            List<List<Integer>> result = gamePropertiesService.getTemplateData(gameId);

            assertEquals(expectedGrid, result);
        }
    }

    @Nested
    class UpdateGameProperties {

        @Test
        void shouldUpdateCharacterAtCalculatedIndex() {
            UUID gameId = UUID.randomUUID();
            // 81 characters representing an empty board
            String initialState = "0".repeat(81);
            GameProperties properties = new GameProperties(gameId, UUID.randomUUID(), initialState);

            when(repository.findById(gameId)).thenReturn(Optional.of(properties));

            // Row 1, Col 2 -> Index: 1 * 9 + 2 = 11
            gamePropertiesService.updateGameProperties(gameId, 1, 2, 5);

            ArgumentCaptor<GameProperties> propertiesCaptor = ArgumentCaptor.forClass(GameProperties.class);
            verify(repository, times(1)).save(propertiesCaptor.capture());

            String updatedState = propertiesCaptor.getValue().getCurrentState();
            assertEquals('5', updatedState.charAt(11));
            assertEquals(81, updatedState.length());
        }

        @ParameterizedTest
        @CsvSource({
                ", 1, 5",
                "1, , 5",
                "1, 1, "
        })
        void shouldThrowExceptionWhenAnyParameterIsNull(Integer row, Integer col, Integer value) {
            UUID gameId = UUID.randomUUID();

            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    gamePropertiesService.updateGameProperties(gameId, row, col, value)
            );

            assertEquals("Row, col, and value must not be null", exception.getMessage());
            verifyNoInteractions(repository);
        }

        @ParameterizedTest
        @CsvSource({
                "-1, 4, 5",
                "9, 4, 5",
                "4, -1, 5",
                "4, 9, 5"
        })
        void shouldThrowExceptionWhenCoordinatesAreOutOfBounds(Integer row, Integer col, Integer value) {
            UUID gameId = UUID.randomUUID();

            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    gamePropertiesService.updateGameProperties(gameId, row, col, value)
            );

            assertEquals("Row and col must be between 0 and 8", exception.getMessage());
            verifyNoInteractions(repository);
        }

        @ParameterizedTest
        @CsvSource({
                "4, 4, -1",
                "4, 4, 10"
        })
        void shouldThrowExceptionWhenValueIsOutOfBounds(Integer row, Integer col, Integer value) {
            UUID gameId = UUID.randomUUID();

            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    gamePropertiesService.updateGameProperties(gameId, row, col, value)
            );

            assertEquals("Value must be between 0 and 9", exception.getMessage());
            verifyNoInteractions(repository);
        }

        @Test
        void shouldDoNothingWhenGamePropertiesNotFound() {
            UUID gameId = UUID.randomUUID();
            when(repository.findById(gameId)).thenReturn(Optional.empty());

            gamePropertiesService.updateGameProperties(gameId, 0, 0, 5);

            verify(repository, never()).save(any(GameProperties.class));
        }
    }
}
