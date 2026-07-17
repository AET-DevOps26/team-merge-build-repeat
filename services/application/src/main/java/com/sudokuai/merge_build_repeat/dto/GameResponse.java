package com.sudokuai.merge_build_repeat.dto;
import java.util.List;
import java.util.UUID;

public record GameResponse(
        List<List<Integer>> templateData,
        List<List<Integer>> solutionData,
        UUID gameId,
        UUID templateId
) {}

