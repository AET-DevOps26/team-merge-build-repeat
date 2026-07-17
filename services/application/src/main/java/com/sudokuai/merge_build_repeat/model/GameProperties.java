package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.UUID;


@Entity
@Table(name = "game_properties")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class GameProperties {
    @Id
    @Column(columnDefinition = "uuid", updatable = false, nullable = false)
    private UUID id; //gameId

    @Column(nullable = false)
    private UUID templateId;

    @Column(nullable = false)
    private String currentState;

    @Column
    private UUID userId;

}
