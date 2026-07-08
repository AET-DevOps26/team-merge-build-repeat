package com.sudokuai.merge_build_repeat.model;

import jakarta.persistence.*;
import lombok.*;


@Entity
@Table(name = "account")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Account {
    @Id
    private Long userId;

    @Column
    private Long gameId;

}