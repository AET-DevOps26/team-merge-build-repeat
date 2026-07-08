package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.exception.NoTemplateException;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GamePropertiesRepository;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.security.SecureRandom;
import java.util.List;

@Service
@AllArgsConstructor
public class GameTemplateService {

    GameTemplateRepository templateRepository;
    GamePropertiesRepository propertiesRepository;
    MapperService mapperService;

    public void saveTemplate(String difficulty, String templateData, String solutionData) {
        GameTemplate template = new GameTemplate();
        template.setDifficulty(difficulty);
        template.setTemplateData(templateData);
        template.setSolutionData(solutionData);
        templateRepository.save(template);
    }

    public GameResponse getRandomGameByDifficulty(String difficulty) {
        GameTemplate template = templateRepository.findByDifficulty(difficulty).stream().findAny().get();
        long game_id = getGameId();

        propertiesRepository.save(new GameProperties(game_id, template.getId(), template.getTemplateData()));
        return new GameResponse(
                mapperService.mapToList(template.getTemplateData()),
                mapperService.mapToList(template.getSolutionData()),
                game_id
        );
    }

    private static long getGameId() {
        SecureRandom secureRandom = new SecureRandom();
        long game_id = Math.abs(secureRandom.nextLong());
        return game_id;
    }

    public GameResponse createNewGameFromTemplate(Long templateId) {
        long game_id = getGameId();
        GameTemplate template = templateRepository.findById(templateId)
                .orElseThrow(() -> new NoTemplateException("Template with ID " + templateId + " not found"));

        propertiesRepository.save(new GameProperties(game_id, template.getId(), template.getTemplateData()));

        return new GameResponse(
                mapperService.mapToList(template.getTemplateData()),
                mapperService.mapToList(template.getSolutionData()),
                game_id
        );
    }


//    public GameTemplate getTemplateByFilename(String filename) {
//        return repository.findByFilename(filename);
//    }


}

