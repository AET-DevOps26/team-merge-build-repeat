package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name = "game_template")
@Getter
@Setter
public class GameTemplate {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String difficulty; //e.g easy, medium, hard

    @Column(nullable = false)
    private String templateData;

    @Column(nullable = false)
    private String solutionData;
}
