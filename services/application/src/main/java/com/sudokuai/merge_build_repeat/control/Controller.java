package com.sudokuai.merge_build_repeat.control;

import com.sudokuai.merge_build_repeat.dto.GameResponse;
import com.sudokuai.merge_build_repeat.dto.*;
import com.sudokuai.merge_build_repeat.dto.UserGameSummary;
import com.sudokuai.merge_build_repeat.model.GameProperties;
import com.sudokuai.merge_build_repeat.service.*;
import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.UUID;


@RestController
@AllArgsConstructor
@RequestMapping("/v1")
public class Controller {

    private static final Logger logger = LoggerFactory.getLogger(Controller.class);

    GameTemplateService gameTemplateService;
    GamePropertiesService gamePropertiesService;
    GameHistoryService gameHistoryService;
    AccountService accountService;
    PencilMarksService pencilMarksService;

    private UUID callerUserId(Jwt jwt) {
        return UUID.fromString(jwt.getSubject());
    }

    private void requireOwnership(UUID gameId, UUID userId) {
        GameProperties game = gamePropertiesService.getGamePropertiesByGameId(gameId);
        if (game == null) throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        if (!userId.equals(game.getUserId())) {
            logger.warn("Denied game access: gameId={}, callerUserId={}, ownerUserId={}", gameId, userId, game.getUserId());
            throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        }
    }

    @Transactional
    @PostMapping("/games/random")
    public ResponseEntity<GameResponse> getRandomGame(@RequestParam String difficulty, @AuthenticationPrincipal Jwt jwt) {
        UUID userId = callerUserId(jwt);
        GameResponse newGame = gameTemplateService.generateNewGameWithDifficulty(difficulty, userId);
        accountService.upsertAccount(userId, newGame.gameId());
        return ResponseEntity.ok(newGame);
    }

    @Transactional
    @PostMapping("/templates/{templateId}/new-game")
    public ResponseEntity<GameResponse> getNewGameByTemplateId(@PathVariable UUID templateId, @AuthenticationPrincipal Jwt jwt) {
        UUID userId = callerUserId(jwt);
        GameResponse newGame = gameTemplateService.createNewGameFromTemplate(templateId, userId);
        accountService.upsertAccount(userId, newGame.gameId());
        return ResponseEntity.ok(newGame);
    }

    @GetMapping("/games/{gameId}/state")
    public ResponseEntity<List<List<Integer>>> getCurrentState(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok((List<List<Integer>>) gamePropertiesService.getCurrentState(gameId));
    }

    @GetMapping("/games/{gameId}/solution")
    public ResponseEntity<List<List<Integer>>> getSolution(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(gamePropertiesService.getSolution(gameId));
    }

    @GetMapping("/games/{gameId}/template")
    public ResponseEntity<List<List<Integer>>> getTemplate(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(gamePropertiesService.getTemplateData(gameId));
    }

    /**
     * Allows trusted internal services to verify ownership while forwarding the
     * caller's JWT.  The user identity is derived from the token, never from a
     * request parameter supplied by the calling service.
     */
    @GetMapping("/games/{gameId}/verify")
    public ResponseEntity<Boolean> verifyGameAccess(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(true);
    }

    @PostMapping("/games/{gameId}/history")
    public ResponseEntity<Boolean> updateGameHistory(@PathVariable UUID gameId, @RequestBody Move move, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        boolean isValid = gameHistoryService.validateAndSaveMove(gameId, move.row(), move.col(), move.value());
        return ResponseEntity.ok(isValid);
    }

    @PutMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<Boolean> updatePencilMarks(@PathVariable UUID gameId, @RequestBody PencilMarkRequest mark, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        boolean isValidInTemplate = pencilMarksService.updatePencilMark(gameId, mark.row(), mark.column(), mark.value());
        return ResponseEntity.ok(isValidInTemplate);
    }

    @DeleteMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<Void> deletePencilMarks(@PathVariable UUID gameId, @RequestParam int row, @RequestParam int col, @RequestParam int value, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        pencilMarksService.deletePencilMark(gameId, row, col, value);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/games/{gameId}/pencil-marks")
    public ResponseEntity<List<List<List<Integer>>>> getCurrentStatePencilMarks(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(pencilMarksService.getPencilMarks(gameId));
    }

    @GetMapping("/games/{gameId}/pencil-mark-history")
    public ResponseEntity<List<PencilMarkHistoryEntry>> getPencilMarkHistory(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(pencilMarksService.getPencilMarkHistory(gameId));
    }

    @Transactional
    @PostMapping("/games/{gameId}/pencil-mark-history")
    public ResponseEntity<Void> savePencilMarkHistory(@PathVariable UUID gameId, @RequestBody SavePencilMarkHistoryRequest req, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        if (req == null || req.row() < 0 || req.row() > 8 || req.column() < 0 || req.column() > 8
                || req.value() < 1 || req.value() > 9 || !("ADD".equals(req.action()) || "REMOVE".equals(req.action()))
                || req.initial() == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid pencil mark history request");
        }
        pencilMarksService.saveToHistory(gameId, req.row(), req.column(), req.value(), req.action(), req.initial());
        return ResponseEntity.noContent().build();
    }

    @Transactional
    @DeleteMapping("/games/{gameId}/pencil-mark-history")
    public ResponseEntity<Void> undoPencilMarkHistory(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        pencilMarksService.undoLastPencilMarkHistory(gameId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/games/{gameId}/history")
    public ResponseEntity<List<HistoryRecord>> getHistory(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        return ResponseEntity.ok(gameHistoryService.getHistoryRecords(gameId));
    }

    @Transactional
    @DeleteMapping("/games/{gameId}/history")
    public ResponseEntity<Void> undoLastMove(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        gameHistoryService.undoLastMove(gameId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/games/{gameId}/info")
    public ResponseEntity<GameInfoResponse> getGameInfo(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        GameProperties gameProperties = gamePropertiesService.getGamePropertiesByGameId(gameId);
        return ResponseEntity.ok(new GameInfoResponse(gameProperties.getTemplateId().toString()));
    }

    @GetMapping("/users/latest-game")
    public ResponseEntity<UUID> getLatestGameId(@AuthenticationPrincipal Jwt jwt) {
        UUID latestGameId = accountService.getLatestGameId(callerUserId(jwt));
        return ResponseEntity.ok(latestGameId);
    }

    @GetMapping("/users/games")
    public ResponseEntity<List<UserGameSummary>> getUserGames(@AuthenticationPrincipal Jwt jwt) {
        return ResponseEntity.ok(gamePropertiesService.getUserGames(callerUserId(jwt)));
    }

    @Transactional
    @DeleteMapping("/games/{gameId}")
    public ResponseEntity<Void> deleteGame(@PathVariable UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        gamePropertiesService.deleteGame(gameId);
        return ResponseEntity.noContent().build();
    }

    // Legacy endpoints kept for backwards compat
    @PostMapping("/users/account")
    public ResponseEntity<Void> createAccount(@AuthenticationPrincipal Jwt jwt) {
        accountService.createAccount(callerUserId(jwt));
        return ResponseEntity.ok().build();
    }

    @PutMapping("/users/account")
    public ResponseEntity<Void> updateAccount(@RequestParam UUID gameId, @AuthenticationPrincipal Jwt jwt) {
        requireOwnership(gameId, callerUserId(jwt));
        accountService.upsertAccount(callerUserId(jwt), gameId);
        return ResponseEntity.ok().build();
    }

    @Transactional
    public void saveAndUpdate(UUID gameId, Move move) {
        gameHistoryService.saveGameHistory(gameId, move.row(), move.col(), move.value());
        gamePropertiesService.updateGameProperties(gameId, move.row(), move.col(), move.value());
    }

}
