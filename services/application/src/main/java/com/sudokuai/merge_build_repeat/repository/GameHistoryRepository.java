package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.GameHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface GameHistoryRepository extends JpaRepository<GameHistory, UUID> {

    List<GameHistory> findByGameIdOrderByCreatedAtAsc(UUID gameId);

    List<GameHistory> findByGameIdIn(List<UUID> gameIds);

    void deleteByGameId(UUID gameId);
}
