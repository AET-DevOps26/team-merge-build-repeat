package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.Collection;


@Entity
@Table(name = "game_properties")
@Getter
@Setter
public class GameProperties {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; //gameId

    @Column(nullable = false)
    private Long templateId;

    @Column(nullable = false)
    private String currentState;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, mappedBy = "gameId")
    private Collection<GameHistory> history;
}