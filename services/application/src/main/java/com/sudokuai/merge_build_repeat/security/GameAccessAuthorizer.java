package com.sudokuai.merge_build_repeat.security;

import com.sudokuai.merge_build_repeat.exception.ForbiddenException;
import com.sudokuai.merge_build_repeat.exception.UnauthorizedException;
import com.sudokuai.merge_build_repeat.service.AccountService;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Component;

import java.util.UUID;


@Component("gameAccessAuthorizer")
public class GameAccessAuthorizer {
    private final AccountService accountService;

    public GameAccessAuthorizer(AccountService accountService) {
        this.accountService = accountService;
    }

    public boolean hasAccess(Authentication authentication, UUID gameId) {
        if (!(authentication instanceof JwtAuthenticationToken jwtAuthentication)) {
            throw new UnauthorizedException("Authentication is required or the provided token is invalid.");
        }

        String subject = jwtAuthentication.getToken().getSubject();
        if (subject == null) {
            throw new UnauthorizedException("Authentication is required or the provided token is invalid.");
        }

        UUID userId;
        try {
            userId = UUID.fromString(subject);
        } catch (IllegalArgumentException exception) {
            throw new UnauthorizedException("Authentication is required or the provided token is invalid.");
        }

        if (!accountService.verifyUserGameAccess(gameId, userId)) {
            throw new ForbiddenException("You do not have access to this game.");
        }
        return true;
    }
}