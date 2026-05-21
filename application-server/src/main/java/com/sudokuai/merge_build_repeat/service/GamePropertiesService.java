package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class GamePropertiesService {

    GamePropertiesRepository repository;

    public Long saveNewGameProperties(Long templateId, String currentState) {
        GameProperties properties = new GameProperties();
        properties.setTemplateId(templateId);
        properties.setCurrentState(currentState);
        repository.save(properties);
        return properties.getId();
    }

    public void updateGameProperties(Long gameId, String currentState) {
        GameProperties properties = repository.findById(gameId).orElse(null);
        if (properties != null) {
            properties.setCurrentState(currentState);
            repository.save(properties);
        }
    }

    public GameProperties getGamePropertiesByGameId(Long gameId) {
         return repository.findById(gameId).orElse(null);
     }

}
