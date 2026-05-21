package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.Collection;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

@Entity
@Table(name = "game_history")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@RequiredArgsConstructor
public class GameHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; //Different for each record

    @Column(nullable = false)
    private Long gameId; //Same for all records of the same game

    @Column(nullable = false)
    private Integer row;

    @Column(nullable = false)
    private Integer col;

    @Column(nullable = false)
    private Integer value;

    public GameHistory(Long gameId, Integer row, Integer col, Integer value) {
        this.gameId = gameId;
        this.row = row;
        this.col = col;
        this.value = value;
    }

    @ManyToOne(cascade = CascadeType.ALL)
    private GameProperties properties;


}