package com.sudokuai.merge_build_repeat.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

public record PencilMark(
        List<Integer> mark
) {
}
