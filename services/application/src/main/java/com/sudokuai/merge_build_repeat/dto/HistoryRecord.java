package com.sudokuai.merge_build_repeat.dto;

import java.time.Instant;
import java.util.UUID;

public record HistoryRecord(UUID id, int row, int col, int value, Instant createdAt) {}
