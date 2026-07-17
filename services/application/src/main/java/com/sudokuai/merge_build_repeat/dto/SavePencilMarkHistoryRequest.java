package com.sudokuai.merge_build_repeat.dto;

public record SavePencilMarkHistoryRequest(int row, int column, int value, String action, Boolean initial) {}
