package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Collection;


@Entity
@Table(name = "game_properties")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class GameProperties {
    @Id
//    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; //gameId

    @Column(nullable = false)
    private Long templateId;

    @Column(nullable = false)
    private String currentState;

}