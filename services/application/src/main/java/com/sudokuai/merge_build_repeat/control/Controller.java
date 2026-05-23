package com.sudokuai.merge_build_repeat.control;

import com.sudokuai.merge_build_repeat.dto.Move;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.service.GameHistoryService;
import com.sudokuai.merge_build_repeat.service.GamePropertiesService;
import com.sudokuai.merge_build_repeat.service.GameTemplateService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@AllArgsConstructor
public class Controller {

    GameTemplateService gameTemplateService;
    GamePropertiesService gamePropertiesService;
    GameHistoryService gameHistoryService;


    @GetMapping(value = "/newTemplate", produces = "text/plain")
    public String newTemplateEndpoint() {
        gameTemplateService.saveTemplate("test_template " + System.currentTimeMillis(), "", "");
        return "You just created a new template! Check the database to see it.";
    }

    @GetMapping(value = "/newGame", produces = "text/plain")
    public Long createNewGameID() {
        Long id = System.currentTimeMillis();

        return id;
    }


    @PutMapping(value = "/updateGame/{gameId}", produces = "text/plain")
    public String updateGame(@PathVariable Long gameId, Move move) {
        gameHistoryService.saveGameHistory(gameId, move.row(), move.col(), move.value());
        gamePropertiesService.updateGameProperties(gameId, "Updated state at " + System.currentTimeMillis());
        return "You just updated a game! Check the database to see it.";
    }

}
