package team_merge_build_repeat.chat_database_service.security;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpHeaders;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import team_merge_build_repeat.chat_database_service.exception.ForbiddenException;
import team_merge_build_repeat.chat_database_service.exception.UnauthorizedException;

import java.util.UUID;

@Component("gameAccessAuthorizer")
public class GameAccessAuthorizer {
	private final GameAccessVerificationClient verificationClient;

	public GameAccessAuthorizer(GameAccessVerificationClient verificationClient) {
		this.verificationClient = verificationClient;
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

		String authorization = incomingAuthorizationHeader();
		if (authorization == null) {
			// This fallback is used outside an HTTP request (for example in a
			// method-security test). Normal service calls always forward the
			// original header unchanged.
			authorization = "Bearer " + jwtAuthentication.getToken().getTokenValue();
		}
		return switch (verificationClient.verify(userId, gameId, authorization)) {
			case ALLOWED -> true;
			case FORBIDDEN -> throw new ForbiddenException("The authenticated user is not allowed to access this game chat.");
			case UNAUTHORIZED -> throw new UnauthorizedException("Authentication is required or the provided token is invalid.");
		};
	}

	private String incomingAuthorizationHeader() {
		if (!(RequestContextHolder.getRequestAttributes() instanceof ServletRequestAttributes attributes)) {
			return null;
		}

		HttpServletRequest request = attributes.getRequest();
		String authorization = request.getHeader(HttpHeaders.AUTHORIZATION);
		return authorization != null && authorization.startsWith("Bearer ") ? authorization : null;
	}
}
