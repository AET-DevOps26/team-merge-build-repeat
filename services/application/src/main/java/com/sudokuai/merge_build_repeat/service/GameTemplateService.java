package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class GameTemplateService {

    GameTemplateRepository repository;

    public void saveTemplate(String difficulty, String templateData, String solutionData) {
        GameTemplate template = new GameTemplate();
        template.setDifficulty(difficulty);
        template.setTemplateData(templateData);
        template.setSolutionData(solutionData);
        repository.save(template);
    }

    public GameResponse getRandomGameByDifficulty(String difficulty) {
        return null;
    }

    public GameResponse createNewGameFromTemplate(Long templateId) {
        return null;
    }


//    public GameTemplate getTemplateByFilename(String filename) {
//        return repository.findByFilename(filename);
//    }
}
