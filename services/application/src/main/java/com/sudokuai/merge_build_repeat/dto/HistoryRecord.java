package com.sudokuai.merge_build_repeat.dto;

public record HistoryRecord(int step, int row, int column, int value, long timestamp) {}
