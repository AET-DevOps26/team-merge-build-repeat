package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.PencilMarks;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface PencilMarksRepository extends JpaRepository<PencilMarks, UUID> {
    PencilMarks findByGameIdAndRowAndCol(UUID gameId, int row, int col);

    List<PencilMarks> findByGameId(UUID gameId);

    void deleteByGameId(UUID gameId);
}
