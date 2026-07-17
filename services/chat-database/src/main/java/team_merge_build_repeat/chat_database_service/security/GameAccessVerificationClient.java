package team_merge_build_repeat.chat_database_service.security;

import java.util.UUID;

public interface GameAccessVerificationClient {
	GameAccessVerificationResult verify(UUID userId, UUID gameId, String authorization);
}
