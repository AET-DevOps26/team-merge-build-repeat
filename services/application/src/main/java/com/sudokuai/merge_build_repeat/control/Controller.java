package com.sudokuai.merge_build_repeat.control;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.dto.*;
//import com.sudokuai.merge_build_repeat.dto.Move;

import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.service.*;
import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;


@RestController
@AllArgsConstructor
@RequestMapping("/v1")
public class Controller {

    GameTemplateService gameTemplateService;
    GamePropertiesService gamePropertiesService;
    GameHistoryService gameHistoryService;
    AccountService accountService;
    PencilMarksService pencilMarksService;


    @GetMapping(value = "/newTemplate", produces = "text/plain")
    public String newTemplateEndpoint() {
        gameTemplateService.saveTemplate("test_template " + System.currentTimeMillis(), "", "");
        return "You just created a new template! Check the database to see it.";
    }

    @PutMapping(value = "/updateGame/{gameId}", produces = "text/plain")
    public String updateGame(@PathVariable UUID gameId, @RequestBody Move move) {
        saveAndUpdate(gameId, move);
        return "You just updated a game! Check the database to see it.";
    }

    @GetMapping("/games/random")
    public ResponseEntity<GameResponse> getRandomGame(@RequestParam String difficulty) {
        GameResponse newGame = gameTemplateService.getRandomGameByDifficulty(difficulty);
        gamePropertiesService.saveNewGameProperties(newGame.gameId(), null, null);
        return ResponseEntity.ok(newGame);
    }

    @GetMapping("/templates/{templateId}/new-game")
    public ResponseEntity<GameResponse> getNewGameByTemplateId(@PathVariable UUID templateId) {
        return ResponseEntity.ok(gameTemplateService.createNewGameFromTemplate(templateId));
    }

    @GetMapping("/games/{gameId}/state")
    public ResponseEntity<List<List<Integer>>> getCurrentState(@PathVariable UUID gameId) {
        return ResponseEntity.ok((List<List<Integer>>) gamePropertiesService.getCurrentState(gameId));
    }

    @GetMapping("/games/{gameId}/solution")
    public ResponseEntity<List<List<Integer>>> getSolution(@PathVariable UUID gameId) {
        return ResponseEntity.ok(gamePropertiesService.getSolution(gameId));
    }

    @GetMapping("/games/{gameId}/template")
    public ResponseEntity<List<List<Integer>>> getTemplate(@PathVariable UUID gameId) {
        return ResponseEntity.ok(gamePropertiesService.getTemplateData(gameId));
    }

    @PostMapping("/games/{gameId}/history")
    public ResponseEntity<Boolean> updateGameHistory(@PathVariable UUID gameId, @RequestBody Move move) {
        boolean isValid = gameHistoryService.validateAndSaveMove(gameId, move.row(), move.col(), move.value());
        return ResponseEntity.ok(isValid);
    }

    @PutMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<Boolean> updatePencilMarks(@PathVariable UUID gameId, @RequestBody PencilMarkRequest mark) {
        boolean isValidInTemplate = pencilMarksService.updatePencilMark(gameId, mark.row(), mark.column(), mark.value());
        return ResponseEntity.ok(isValidInTemplate);
    }

    @DeleteMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<Void> deletePencilMarks(@PathVariable UUID gameId, @RequestBody PencilMarkRequest mark) {
        pencilMarksService.deletePencilMark(gameId, mark.row(), mark.column(), mark.value());
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<List<List<List<Integer>>>> getCurrentStatePencilMarks(@PathVariable UUID gameId) {
        return ResponseEntity.ok(pencilMarksService.getPencilMarks(gameId));
    }

    @GetMapping("/games/{gameId}/history")
    public ResponseEntity<List<HistoryRecord>> getHistory(@PathVariable UUID gameId) {
        return ResponseEntity.ok(gameHistoryService.getHistoryRecords(gameId));
    }

    @PostMapping("/users/account")
    public ResponseEntity<Void> createAccount(UUID userId) {
        accountService.createAccount(userId);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/users/account")
    public ResponseEntity<Void> updateAccount(UUID userId, UUID gameId) {
        accountService.updateAccount(userId, gameId);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/users/latest-game")
    public ResponseEntity<UUID> getLatestGameId(@RequestParam UUID userId) {
        UUID latestGameId = accountService.getLatestGameId(userId);
        return ResponseEntity.ok(latestGameId);
    }

    @GetMapping("/games/{gameId}/verify")
    public ResponseEntity<Boolean> verifyGameId(@PathVariable UUID gameId, @RequestParam UUID userId) {
        boolean isValid = accountService.verifyUserGameAccess(gameId, userId);
        return ResponseEntity.ok(isValid);
    }

    @Transactional
    public void saveAndUpdate(UUID gameId, Move move) {
        gameHistoryService.saveGameHistory(gameId, move.row(), move.col(), move.value());
        gamePropertiesService.updateGameProperties(gameId, move.row(), move.col(), move.value());
    }

}
