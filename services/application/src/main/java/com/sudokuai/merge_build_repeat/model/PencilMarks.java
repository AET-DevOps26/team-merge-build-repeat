package com.sudokuai.merge_build_repeat.model;

import com.sudokuai.merge_build_repeat.dto.PencilMark;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.*;


@Entity
@Table(name = "pencil_marks")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class PencilMarks {
    @Id
    @GeneratedValue
    @Column(columnDefinition = "uuid", updatable = false, nullable = false)
    private UUID id;

    @Column
    private UUID gameId;

    @Column
    private int row;

    @Column
    private int col;

    @Column
    private String marks;

}