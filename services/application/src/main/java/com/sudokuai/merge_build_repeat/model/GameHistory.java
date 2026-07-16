package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.UUID;


@Entity
@Table(name = "game_history")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class GameHistory {
    @Id
    @GeneratedValue
    @Column(columnDefinition = "uuid", updatable = false, nullable = false)
    private UUID id; //Different for each record

    @Column(nullable = false)
    private UUID gameId; //Same for all records of the same game

    @Column(nullable = false)
    private Integer row;

    @Column(nullable = false)
    private Integer col;

    @Column(nullable = false)
    private Integer value;

    public GameHistory(UUID gameId, Integer row, Integer col, Integer value) {
        this.gameId = gameId;
        this.row = row;
        this.col = col;
        this.value = value;
    }
}