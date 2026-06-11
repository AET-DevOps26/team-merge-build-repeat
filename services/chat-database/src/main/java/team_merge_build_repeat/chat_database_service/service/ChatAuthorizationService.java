package team_merge_build_repeat.chat_database_service.service;

import java.util.UUID;

public interface ChatAuthorizationService {
	void ensureReadable(UUID gameId);

	void ensureWritable(UUID gameId);
}
