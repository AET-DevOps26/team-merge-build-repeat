package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.PencilMarks;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PencilMarksRepository extends JpaRepository<PencilMarks, Long> {
    PencilMarks findByGameIdAndRowAndCol(Long gameId, int row, int col);

    List<PencilMarks> findByGameId(Long gameId);
}
