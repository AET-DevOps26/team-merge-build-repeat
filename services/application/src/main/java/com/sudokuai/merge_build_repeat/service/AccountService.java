package com.sudokuai.merge_build_repeat.service;

import com.sudokuai.merge_build_repeat.dto.HistoryRecord;
import com.sudokuai.merge_build_repeat.model.Account;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import com.sudokuai.merge_build_repeat.repository.AccountRepository;
import com.sudokuai.merge_build_repeat.repository.GameHistoryRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@AllArgsConstructor
public class AccountService {

    AccountRepository repository;

    public void createAccount(UUID userId) {
        repository.save(new Account(userId, null));
    }

    public void updateAccount(UUID userId, UUID gameId) {
        repository.save(new Account(userId, gameId));
    }


    public UUID getLatestGameId(UUID userId) {
        Account account = repository.findById(userId).orElseThrow(() -> new RuntimeException("Account not found for userId: " + userId));
        return account.getGameId();
    }

    public boolean verifyUserGameAccess(UUID gameId, UUID userId) {
        Account account = repository.findById(userId).orElseThrow(() -> new RuntimeException("Account not found for userId: " + userId));
        return account.getGameId() != null && account.getGameId().equals(gameId);
    }
}

