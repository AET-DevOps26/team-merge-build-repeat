package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.UUID;

public interface AccountRepository extends JpaRepository<Account, UUID> {

    @Modifying
    @Query(value = "INSERT INTO account (user_id, game_id) VALUES (:userId, :gameId) ON CONFLICT (user_id) DO UPDATE SET game_id = :gameId", nativeQuery = true)
    void upsert(@Param("userId") UUID userId, @Param("gameId") UUID gameId);

    @Modifying
    @Query("UPDATE Account account SET account.gameId = NULL WHERE account.gameId = :gameId")
    void clearLatestGameId(@Param("gameId") UUID gameId);

}
