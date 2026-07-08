package com.sudokuai.merge_build_repeat.repository;

import com.sudokuai.merge_build_repeat.model.Account;
import com.sudokuai.merge_build_repeat.model.GameHistory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AccountRepository extends JpaRepository<Account, Long> {

}
