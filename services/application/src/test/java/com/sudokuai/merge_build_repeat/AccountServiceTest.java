package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.model.Account;
import com.sudokuai.merge_build_repeat.repository.AccountRepository;
import com.sudokuai.merge_build_repeat.service.AccountService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AccountServiceTest {

    @Mock
    private AccountRepository repository;

    @InjectMocks
    private AccountService accountService;

    @Nested
    class CreateAccount {

        @Test
        void shouldCreateAccountWhenUserDoesNotExist() {
            UUID userId = UUID.randomUUID();
            when(repository.existsById(userId)).thenReturn(false);

            accountService.createAccount(userId);

            ArgumentCaptor<Account> accountCaptor = ArgumentCaptor.forClass(Account.class);
            verify(repository, times(1)).save(accountCaptor.capture());

            Account savedAccount = accountCaptor.getValue();
            assertEquals(userId, savedAccount.getUserId());
            assertNull(savedAccount.getGameId());
        }

        @Test
        void shouldThrowExceptionWhenAccountAlreadyExists() {
            UUID userId = UUID.randomUUID();
            when(repository.existsById(userId)).thenReturn(true);

            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    accountService.createAccount(userId)
            );

            assertEquals("Account already exists for userId: " + userId, exception.getMessage());
            verify(repository, never()).save(any(Account.class));
        }
    }

    @Nested
    class UpdateAccount {

        @Test
        void shouldUpdateAccountWithNewGameId() {
            UUID userId = UUID.randomUUID();
            UUID gameId = UUID.randomUUID();

            accountService.updateAccount(userId, gameId);

            ArgumentCaptor<Account> accountCaptor = ArgumentCaptor.forClass(Account.class);
            verify(repository, times(1)).save(accountCaptor.capture());

            Account savedAccount = accountCaptor.getValue();
            assertEquals(userId, savedAccount.getUserId());
            assertEquals(gameId, savedAccount.getGameId());
        }
    }

    @Nested
    class GetLatestGameId {

        @Test
        void shouldReturnGameIdWhenAccountExists() {
            UUID userId = UUID.randomUUID();
            UUID gameId = UUID.randomUUID();
            Account account = new Account(userId, gameId);
            when(repository.findById(userId)).thenReturn(Optional.of(account));

            UUID result = accountService.getLatestGameId(userId);

            assertEquals(gameId, result);
        }

        @Test
        void shouldReturnNullWhenAccountExistsButHasNoGameId() {
            UUID userId = UUID.randomUUID();
            Account account = new Account(userId, null);
            when(repository.findById(userId)).thenReturn(Optional.of(account));

            UUID result = accountService.getLatestGameId(userId);

            assertNull(result);
        }

//        @Test
//        void shouldThrowExceptionWhenAccountDoesNotExist() {
//            UUID userId = UUID.randomUUID();
//            when(repository.findById(userId)).thenReturn(Optional.empty());
//
//            RuntimeException exception = assertThrows(RuntimeException.class, () ->
//                    accountService.getLatestGameId(userId)
//            );
//
//            assertEquals("Account not found for userId: " + userId, exception.getMessage());
//        }
    }

    @Nested
    class VerifyUserGameAccess {

        @Test
        void shouldReturnTrueWhenGameIdMatches() {
            UUID userId = UUID.randomUUID();
            UUID gameId = UUID.randomUUID();
            Account account = new Account(userId, gameId);
            when(repository.findById(userId)).thenReturn(Optional.of(account));

            boolean hasAccess = accountService.verifyUserGameAccess(gameId, userId);

            assertTrue(hasAccess);
        }

        @Test
        void shouldReturnFalseWhenGameIdMismatches() {
            UUID userId = UUID.randomUUID();
            UUID gameId = UUID.randomUUID();
            UUID differentGameId = UUID.randomUUID();
            Account account = new Account(userId, differentGameId);
            when(repository.findById(userId)).thenReturn(Optional.of(account));

            boolean hasAccess = accountService.verifyUserGameAccess(gameId, userId);

            assertFalse(hasAccess);
        }

        @Test
        void shouldReturnFalseWhenAccountHasNoGameId() {
            UUID userId = UUID.randomUUID();
            UUID gameId = UUID.randomUUID();
            Account account = new Account(userId, null);
            when(repository.findById(userId)).thenReturn(Optional.of(account));

            boolean hasAccess = accountService.verifyUserGameAccess(gameId, userId);

            assertFalse(hasAccess);
        }

//        @Test
//        void shouldThrowExceptionWhenAccountDoesNotExist() {
//            UUID userId = UUID.randomUUID();
//            UUID gameId = UUID.randomUUID();
//            when(repository.findById(userId)).thenReturn(Optional.empty());
//
//            RuntimeException exception = assertThrows(RuntimeException.class, () ->
//                    accountService.verifyUserGameAccess(gameId, userId)
//            );
//
//            assertEquals("Account not found for userId: " + userId, exception.getMessage());
//        }
    }
}
