package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.GameTemplate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface GameTemplateRepository extends JpaRepository<GameTemplate, UUID> {
//    GameTemplate findByFilename(String filename);
    List<GameTemplate> findByDifficulty(String difficulty);

}