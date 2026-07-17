package team_merge_build_repeat.chat_database_service.security;

import org.springframework.stereotype.Component;
import org.springframework.http.HttpHeaders;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.UUID;

@Component
public class DefaultGameAccessVerificationClient implements GameAccessVerificationClient {
	private final RestClient applicationServiceRestClient;

	public DefaultGameAccessVerificationClient(RestClient applicationServiceRestClient) {
		this.applicationServiceRestClient = applicationServiceRestClient;
	}

	@Override
	public GameAccessVerificationResult verify(UUID userId, UUID gameId, String authorization) {
		try {
			return applicationServiceRestClient.get()
					.uri(uriBuilder -> uriBuilder
							.path("/v1/games/{gameId}/verify")
							.build(gameId))
					.header(HttpHeaders.AUTHORIZATION, authorization)
					.exchange((request, response) -> switch (response.getStatusCode().value()) {
						case 200 -> Boolean.TRUE.equals(response.bodyTo(Boolean.class))
								? GameAccessVerificationResult.ALLOWED
								: GameAccessVerificationResult.FORBIDDEN;
						case 401 -> GameAccessVerificationResult.UNAUTHORIZED;
						case 403 -> GameAccessVerificationResult.FORBIDDEN;
						case 404 -> GameAccessVerificationResult.FORBIDDEN;
						default -> throw new GameVerificationUnavailableException(
								"The game access verification service returned " + response.getStatusCode() + ".", null);
					});
		} catch (GameVerificationUnavailableException exception) {
			throw exception;
		} catch (RestClientException exception) {
			throw new GameVerificationUnavailableException("The game access verification service is unavailable.", exception);
		}
	}
}
