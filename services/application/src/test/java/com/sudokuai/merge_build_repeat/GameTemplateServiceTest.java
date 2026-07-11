package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.exception.NoTemplateException;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import com.sudokuai.merge_build_repeat.service.GameTemplateService;
import com.sudokuai.merge_build_repeat.service.MapperService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class GameTemplateServiceTest {

    @Mock
    private GameTemplateRepository templateRepository;

    @Mock
    private GamePropertiesRepository propertiesRepository;

    @Mock
    private MapperService mapperService;

    @InjectMocks
    private GameTemplateService gameTemplateService;

    @Nested
    class SaveTemplate {

        @Test
        void shouldSaveTemplateWithCorrectFields() {
            String difficulty = "HARD";
            String templateData = "003000...".repeat(9);
            String solutionData = "413925...".repeat(9);

            gameTemplateService.saveTemplate(difficulty, templateData, solutionData);

            ArgumentCaptor<GameTemplate> templateCaptor = ArgumentCaptor.forClass(GameTemplate.class);
            verify(templateRepository, times(1)).save(templateCaptor.capture());

            GameTemplate savedTemplate = templateCaptor.getValue();
            assertEquals(difficulty, savedTemplate.getDifficulty());
            assertEquals(templateData, savedTemplate.getTemplateData());
            assertEquals(solutionData, savedTemplate.getSolutionData());
        }
    }

    @Nested
    class GetRandomGameByDifficulty {

        @Test
        void shouldReturnGameResponseAndSavePropertiesWhenTemplateExists() {
            String difficulty = "MEDIUM";
            UUID templateId = UUID.randomUUID();
            String templateDataStr = "050200...";
            String solutionDataStr = "154236...";

            GameTemplate mockTemplate = new GameTemplate();
            mockTemplate.setId(templateId);
            mockTemplate.setDifficulty(difficulty);
            mockTemplate.setTemplateData(templateDataStr);
            mockTemplate.setSolutionData(solutionDataStr);

            List<List<Integer>> expectedTemplateGrid = List.of(List.of(0, 5, 0));
            List<List<Integer>> expectedSolutionGrid = List.of(List.of(1, 5, 4));

            when(templateRepository.findByDifficulty(difficulty)).thenReturn(List.of(mockTemplate));
            when(mapperService.mapToList(templateDataStr)).thenReturn(expectedTemplateGrid);
            when(mapperService.mapToList(solutionDataStr)).thenReturn(expectedSolutionGrid);

            GameResponse response = gameTemplateService.getRandomGameByDifficulty(difficulty);

            assertNotNull(response);
            assertEquals(expectedTemplateGrid, response.templateData()); // Assuming record style accessors or standard getters
            assertEquals(expectedSolutionGrid, response.solutionData());
            assertNotNull(response.gameId());

            ArgumentCaptor<GameProperties> propertiesCaptor = ArgumentCaptor.forClass(GameProperties.class);
            verify(propertiesRepository, times(1)).save(propertiesCaptor.capture());

            GameProperties savedProperties = propertiesCaptor.getValue();
            assertEquals(response.gameId(), savedProperties.getId()); // Verifies generated UUID matches across components
            assertEquals(templateId, savedProperties.getTemplateId());
            assertEquals(templateDataStr, savedProperties.getCurrentState());
        }

        @Test
        void shouldThrowNoTemplateExceptionWhenNoTemplatesMatchDifficulty() {
            String difficulty = "EXPERT";
            when(templateRepository.findByDifficulty(difficulty)).thenReturn(Collections.emptyList());

            NoTemplateException exception = assertThrows(NoTemplateException.class, () ->
                    gameTemplateService.getRandomGameByDifficulty(difficulty)
            );

            assertEquals("No template found for difficulty: " + difficulty, exception.getMessage());
            verifyNoInteractions(propertiesRepository, mapperService);
        }
    }

    @Nested
    class CreateNewGameFromTemplate {

        @Test
        void shouldCreateGameFromTemplateWhenIdExists() {
            UUID templateId = UUID.randomUUID();
            String templateDataStr = "700001...";
            String solutionDataStr = "723451...";

            GameTemplate mockTemplate = new GameTemplate();
            mockTemplate.setId(templateId);
            mockTemplate.setTemplateData(templateDataStr);
            mockTemplate.setSolutionData(solutionDataStr);

            List<List<Integer>> expectedTemplateGrid = List.of(List.of(7, 0, 0));
            List<List<Integer>> expectedSolutionGrid = List.of(List.of(7, 2, 3));

            when(templateRepository.findById(templateId)).thenReturn(Optional.of(mockTemplate));
            when(mapperService.mapToList(templateDataStr)).thenReturn(expectedTemplateGrid);
            when(mapperService.mapToList(solutionDataStr)).thenReturn(expectedSolutionGrid);

            GameResponse response = gameTemplateService.createNewGameFromTemplate(templateId);

            assertNotNull(response);
            assertEquals(expectedTemplateGrid, response.templateData());
            assertEquals(expectedSolutionGrid, response.solutionData());
            assertNotNull(response.gameId());

            ArgumentCaptor<GameProperties> propertiesCaptor = ArgumentCaptor.forClass(GameProperties.class);
            verify(propertiesRepository, times(1)).save(propertiesCaptor.capture());

            GameProperties savedProperties = propertiesCaptor.getValue();
            assertEquals(response.gameId(), savedProperties.getId());
            assertEquals(templateId, savedProperties.getTemplateId());
            assertEquals(templateDataStr, savedProperties.getCurrentState());
        }

        @Test
        void shouldThrowNoTemplateExceptionWhenTemplateIdNotFound() {
            UUID templateId = UUID.randomUUID();
            when(templateRepository.findById(templateId)).thenReturn(Optional.empty());

            NoTemplateException exception = assertThrows(NoTemplateException.class, () ->
                    gameTemplateService.createNewGameFromTemplate(templateId)
            );

            assertEquals("Template with ID " + templateId + " not found", exception.getMessage());
            verifyNoInteractions(propertiesRepository, mapperService);
        }
    }
}
