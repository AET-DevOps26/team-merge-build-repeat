package com.sudokuai.merge_build_repeat.model;

import com.sudokuai.merge_build_repeat.dto.PencilMark;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;


@Entity
@Table(name = "pencil_marks")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class PencilMarks {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private Long gameId;

    @Column
    private int row;

    @Column
    private int col;

    @Column
    private String marks;

}