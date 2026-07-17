package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "pencil_mark_history")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class PencilMarkHistory {
    @Id
    @GeneratedValue
    @Column(columnDefinition = "uuid", updatable = false, nullable = false)
    private UUID id;

    @Column(nullable = false)
    private UUID gameId;

    @Column(nullable = false)
    private int row;

    @Column(nullable = false)
    private int col;

    @Column(nullable = false)
    private int value;

    @Column(nullable = false)
    private String action; // "ADD" or "REMOVE"

    @Column(nullable = false)
    private boolean initial;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    public PencilMarkHistory(UUID gameId, int row, int col, int value, String action, boolean initial) {
        this.gameId = gameId;
        this.row = row;
        this.col = col;
        this.value = value;
        this.action = action;
        this.initial = initial;
    }
}
