package com.sudokuai.merge_build_repeat.dto;
import java.util.List;

public record GameResponse(List<List<Integer>> templateData, List<List<Integer>> solutionData, Long gameId) {}

