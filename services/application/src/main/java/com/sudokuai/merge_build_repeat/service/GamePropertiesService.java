package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.UserGameSummary;
import com.sudokuai.merge_build_repeat.exception.NoTemplateException;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.AccountRepository;
import com.sudokuai.merge_build_repeat.repository.GameHistoryRepository;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import com.sudokuai.merge_build_repeat.repository.PencilMarkHistoryRepository;
import com.sudokuai.merge_build_repeat.repository.PencilMarksRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class GamePropertiesService {

    GamePropertiesRepository repository;
    GameTemplateRepository templateRepository;
    GameHistoryRepository gameHistoryRepository;
    PencilMarkHistoryRepository pencilMarkHistoryRepository;
    PencilMarksRepository pencilMarksRepository;
    AccountRepository accountRepository;
    MapperService mapperService;

//    public void updateGameProperties(UUID gameId, String currentState) {
//        GameProperties properties = repository.findById(gameId).orElse(null);
//        if (properties != null) {
//            properties.setCurrentState(currentState);
//            repository.save(properties);
//        }
//    }

    public GameProperties getGamePropertiesByGameId(UUID gameId) {
         return repository.findById(gameId).orElse(null);
     }

    public List<List<Integer>> getCurrentState(UUID gameId) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            String currentState = properties.getCurrentState();
            return mapperService.mapToList(currentState);
        }
        return null;
    }

    public List<List<Integer>> getSolution(UUID gameId) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            GameTemplate template = templateRepository.findById(properties.getTemplateId())
                    .orElseThrow(() -> new NoTemplateException("Template with ID " + properties.getTemplateId() + " not found"));
            String solution = template.getSolutionData();
            return mapperService.mapToList(solution);
        }
        return null;
    }

    public List<List<Integer>> getTemplateData(UUID gameId) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            GameTemplate template = templateRepository.findById(properties.getTemplateId())
                    .orElseThrow(() -> new NoTemplateException("Template with ID " + properties.getTemplateId() + " not found"));
            String templateData = template.getTemplateData();
            return mapperService.mapToList(templateData);
        }
        return null;
    }

    public boolean isEditableCell(UUID gameId, int row, int col) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties == null) {
            return false;
        }

        GameTemplate template = templateRepository.findById(properties.getTemplateId()).orElse(null);
        if (template == null || template.getTemplateData().length() != 81) {
            return false;
        }

        return template.getTemplateData().charAt(row * 9 + col) == '0';
    }

//    public void updateGameProperties(UUID gameId, Integer row, Integer col, Integer value) {
//        GameProperties properties = repository.findById(gameId).orElse(null);
//        if (properties != null) {
//            String currentState = properties.getCurrentState();
//            StringBuilder sb = new StringBuilder(currentState);
//            sb.setCharAt(row * 9 + col, value.toString().charAt(0));
//            String result = sb.toString();
//            properties.setCurrentState(result);
//            repository.save(properties);
//        }

    public void updateGameProperties(UUID gameId, Integer row, Integer col, Integer value) {
        if (row == null || col == null || value == null) {
            throw new IllegalArgumentException("Row, col, and value must not be null");
        }
        if (row < 0 || row > 8 || col < 0 || col > 8) {
            throw new IllegalArgumentException("Row and col must be between 0 and 8");
        }
        if (value < 0 || value > 9) {
            throw new IllegalArgumentException("Value must be between 0 and 9");
        }
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            String currentState = properties.getCurrentState();
            StringBuilder sb = new StringBuilder(currentState);
            sb.setCharAt(row * 9 + col, value.toString().charAt(0));
            String result = sb.toString();
            properties.setCurrentState(result);
            repository.save(properties);
        }
    }

    @Transactional
    public void deleteGame(UUID gameId) {
        GameProperties deletedGame = repository.findById(gameId).orElse(null);
        UUID replacementGameId = deletedGame == null || deletedGame.getUserId() == null
                ? null
                : repository.findByUserIdOrderByIdAsc(deletedGame.getUserId()).stream()
                        .map(GameProperties::getId)
                        .filter(id -> !id.equals(gameId))
                        .findFirst()
                        .orElse(null);
        accountRepository.replaceLatestGameId(gameId, replacementGameId);
        gameHistoryRepository.deleteByGameId(gameId);
        pencilMarkHistoryRepository.deleteByGameId(gameId);
        pencilMarksRepository.deleteByGameId(gameId);
        repository.deleteById(gameId);
    }

    public List<UserGameSummary> getUserGames(UUID userId) {
        List<GameProperties> games = repository.findByUserIdOrderByIdAsc(userId);
        List<UUID> templateIds = games.stream().map(GameProperties::getTemplateId).distinct().toList();
        List<UUID> gameIds = games.stream().map(GameProperties::getId).toList();
        Map<UUID, GameTemplate> templatesById = templateRepository.findAllById(templateIds).stream()
                .collect(Collectors.toMap(GameTemplate::getId, Function.identity()));
        Map<UUID, List<GameHistory>> historiesByGameId = gameHistoryRepository.findByGameIdIn(gameIds).stream()
                .collect(Collectors.groupingBy(GameHistory::getGameId));

        return games.stream().map(game -> {
            GameTemplate template = templatesById.get(game.getTemplateId());
            String difficulty = template != null ? template.getDifficulty() : "unknown";
            String templateData = template != null ? template.getTemplateData() : "";

            // Count empty cells in template
            int totalCells = 0;
            for (int i = 0; i < templateData.length(); i++) {
                if (templateData.charAt(i) == '0') totalCells++;
            }

            // Compute filled cells from game_history: latest value per (row,col)
            int[] latestValues = new int[81]; // 0 = empty
            historiesByGameId.getOrDefault(game.getId(), List.of()).stream()
                .sorted(Comparator.comparing(GameHistory::getCreatedAt, Comparator.nullsFirst(Comparator.naturalOrder())))
                .forEach(h -> latestValues[h.getRow() * 9 + h.getCol()] = h.getValue());
            int filledCells = 0;
            for (int i = 0; i < templateData.length(); i++) {
                if (templateData.charAt(i) == '0' && latestValues[i] != 0) filledCells++;
            }

            return new UserGameSummary(game.getId(), game.getTemplateId(), difficulty, filledCells, totalCells);
        }).toList();
    }

    @Transactional
    public void recalculateStateFromHistory(UUID gameId) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties == null) return;

        GameTemplate template = templateRepository.findById(properties.getTemplateId())
                .orElseThrow(() -> new NoTemplateException("Template with ID " + properties.getTemplateId() + " not found"));

        String templateData = template.getTemplateData();
        StringBuilder currentState = new StringBuilder(templateData);

        List<GameHistory> history = gameHistoryRepository.findByGameIdOrderByCreatedAtAsc(gameId);
        for (GameHistory h : history) {
            currentState.setCharAt(h.getRow() * 9 + h.getCol(), h.getValue().toString().charAt(0));
        }

        properties.setCurrentState(currentState.toString());
        repository.save(properties);
    }
}
