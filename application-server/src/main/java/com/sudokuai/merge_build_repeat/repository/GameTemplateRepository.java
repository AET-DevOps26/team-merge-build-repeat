package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.GameTemplate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GameTemplateRepository extends JpaRepository<GameTemplate, Long> {
    GameTemplate findByFilename(String filename);

}