package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.GameHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GameHistoryRepository extends JpaRepository<GameHistory, Long> {

    List<GameHistory> findByGameId(Long gameId);
}