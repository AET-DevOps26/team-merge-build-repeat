package team_merge_build_repeat.chat_database_service.service;

import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class DefaultChatAuthorizationService implements ChatAuthorizationService {
	@Override
	public void ensureReadable(UUID gameId) {
	}

	@Override
	public void ensureWritable(UUID gameId) {
	}
}
