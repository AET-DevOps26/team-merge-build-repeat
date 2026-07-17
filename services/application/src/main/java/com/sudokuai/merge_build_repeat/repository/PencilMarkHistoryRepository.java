package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.PencilMarkHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface PencilMarkHistoryRepository extends JpaRepository<PencilMarkHistory, UUID> {
    List<PencilMarkHistory> findByGameIdOrderByCreatedAtAsc(UUID gameId);

    void deleteByGameId(UUID gameId);
}
