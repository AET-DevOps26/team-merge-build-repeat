package team_merge_build_repeat.chat_database_service.security;

import org.springframework.stereotype.Component;
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
	public GameAccessVerificationResult verify(String bearerToken, UUID gameId) {
		try {
			return applicationServiceRestClient.post()
					.uri("/v1/games/{gameId}/verify", gameId)
					.header("Authorization", "Bearer " + bearerToken)
					.exchange((request, response) -> switch (response.getStatusCode().value()) {
						case 204 -> GameAccessVerificationResult.ALLOWED;
						case 401 -> GameAccessVerificationResult.UNAUTHORIZED;
						case 403 -> GameAccessVerificationResult.FORBIDDEN;
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
