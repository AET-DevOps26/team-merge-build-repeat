package com.sudokuai.merge_build_repeat.dto;

import java.util.UUID;

public record UserGameSummary(UUID gameId, UUID templateId, String difficulty, int filledCells, int totalCells) {}
