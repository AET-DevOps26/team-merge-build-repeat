package com.sudokuai.merge_build_repeat.dto;

import java.time.Instant;

public record PencilMarkHistoryEntry(int row, int col, int value, String action, boolean initial, Instant createdAt) {}
