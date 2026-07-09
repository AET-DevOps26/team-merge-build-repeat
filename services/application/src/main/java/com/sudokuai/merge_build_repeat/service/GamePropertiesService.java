package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class GamePropertiesService {

    GamePropertiesRepository repository;
    GameTemplateRepository templateRepository;
    MapperService mapperService;

    public UUID saveNewGameProperties(UUID templateId, String currentState) {
        GameProperties properties = new GameProperties();
        properties.setTemplateId(templateId);
        properties.setCurrentState(currentState);
        repository.save(properties);
        return properties.getId();
    }

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
            GameTemplate template = templateRepository.findById(properties.getTemplateId()).orElse(null);
            String solution = template.getSolutionData();
            return mapperService.mapToList(solution);
        }
        return null;
    }

    public List<List<Integer>> getTemplateData(UUID gameId) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            GameTemplate template = templateRepository.findById(properties.getTemplateId()).orElse(null);
            String templateData = template.getTemplateData();
            return mapperService.mapToList(templateData);
        }
        return null;
    }

    public void updateGameProperties(UUID gameId, Integer row, Integer col, Integer value) {
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
}
