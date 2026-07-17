package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.exception.NoTemplateException;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.security.SecureRandom;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class GameTemplateService {

    private final GameTemplateRepository templateRepository;
    private final GamePropertiesRepository propertiesRepository;
    private final MapperService mapperService;
    private final RestTemplate restTemplate;

    @Value("${game-engine.url:http://game-engine:8080}")
    private String gameEngineUrl;

    public GameTemplateService(GameTemplateRepository templateRepository, GamePropertiesRepository propertiesRepository, MapperService mapperService, RestTemplate restTemplate) {
        this.templateRepository = templateRepository;
        this.propertiesRepository = propertiesRepository;
        this.mapperService = mapperService;
        this.restTemplate = restTemplate;
    }

    public void saveTemplate(String difficulty, String templateData, String solutionData) {
        GameTemplate template = new GameTemplate();
        template.setDifficulty(difficulty);
        template.setTemplateData(templateData);
        template.setSolutionData(solutionData);
        templateRepository.save(template);
    }

    public GameResponse getRandomGameByDifficulty(String difficulty) {
        return getRandomGameByDifficulty(difficulty, null);
    }

    public GameResponse getRandomGameByDifficulty(String difficulty, UUID userId) {
//        GameTemplate template = templateRepository.findByDifficulty(difficulty).stream().findAny().get();
        GameTemplate template = templateRepository.findByDifficulty(difficulty).stream()
                .findAny()
                .orElseThrow(() -> new NoTemplateException("No template found for difficulty: " + difficulty));
        UUID game_id = getGameId();

        GameProperties props = new GameProperties(game_id, template.getId(), template.getTemplateData(), userId);
        propertiesRepository.save(props);
        return new GameResponse(
                mapperService.mapToList(template.getTemplateData()),
                mapperService.mapToList(template.getSolutionData()),
                game_id,
                template.getId()
        );
    }

    private static UUID getGameId() {
        SecureRandom secureRandom = new SecureRandom();
        UUID game_id = new UUID(secureRandom.nextLong(), secureRandom.nextLong());
        return game_id;
    }

    public GameResponse createNewGameFromTemplate(UUID templateId) {
        return createNewGameFromTemplate(templateId, null);
    }

    public GameResponse createNewGameFromTemplate(UUID templateId, UUID userId) {
        UUID game_id = getGameId();
        GameTemplate template = templateRepository.findById(templateId)
                .orElseThrow(() -> new NoTemplateException("Template with ID " + templateId + " not found"));

        propertiesRepository.save(new GameProperties(game_id, template.getId(), template.getTemplateData(), userId));

        return new GameResponse(
                mapperService.mapToList(template.getTemplateData()),
                mapperService.mapToList(template.getSolutionData()),
                game_id,
                template.getId()
        );
    }

    public GameResponse generateNewGameWithDifficulty(String difficulty) {
        return generateNewGameWithDifficulty(difficulty, null);
    }

    public GameResponse generateNewGameWithDifficulty(String difficulty, UUID userId) {
        try {
            String gameEngineEndpoint = gameEngineUrl + "/sudoku?difficulty=" + difficulty;
            Map<String, Object> response = restTemplate.getForObject(gameEngineEndpoint, Map.class);

            if (response == null || !response.containsKey("sudoku")) {
                throw new RuntimeException("Invalid response from game engine");
            }

            List<List<Integer>> sudokuBoard = (List<List<Integer>>) response.get("sudoku");

            // Convert nulls to 0 for the mapper
            List<List<Integer>> boardWithZeros = new java.util.ArrayList<>();
            for (List<Integer> row : sudokuBoard) {
                List<Integer> newRow = new java.util.ArrayList<>();
                for (Integer val : row) {
                    newRow.add(val == null ? 0 : val);
                }
                boardWithZeros.add(newRow);
            }

            String templateData = mapperService.mapToString(boardWithZeros);

            String solutionEndpoint = gameEngineUrl + "/solution";
            Map<String, Object> solutionRequest = Map.of("sudoku", boardWithZeros);
            Map<String, Object> solutionResponse = restTemplate.postForObject(solutionEndpoint, solutionRequest, Map.class);

            if (solutionResponse == null || !solutionResponse.containsKey("sudoku")) {
                throw new RuntimeException("Invalid response from game engine solution");
            }

            List<List<Integer>> solutionBoard = (List<List<Integer>>) solutionResponse.get("sudoku");
            String solutionData = mapperService.mapToString(solutionBoard);

            GameTemplate newTemplate = new GameTemplate();
            newTemplate.setDifficulty(difficulty);
            newTemplate.setTemplateData(templateData);
            newTemplate.setSolutionData(solutionData);
            newTemplate = templateRepository.save(newTemplate);

            UUID gameId = getGameId();
            propertiesRepository.save(new GameProperties(gameId, newTemplate.getId(), templateData, userId));

            return new GameResponse(
                    boardWithZeros,
                    solutionBoard,
                    gameId,
                    newTemplate.getId()
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate game from game engine: " + e.getMessage(), e);
        }
    }


//    public GameTemplate getTemplateByFilename(String filename) {
//        return repository.findByFilename(filename);
//    }


}

