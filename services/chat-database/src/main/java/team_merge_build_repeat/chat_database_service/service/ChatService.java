package team_merge_build_repeat.chat_database_service.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import team_merge_build_repeat.chat_database_service.dto.ChatMessageResponse;
import team_merge_build_repeat.chat_database_service.dto.ChatResponse;
import team_merge_build_repeat.chat_database_service.dto.CreateChatMessageRequest;
import team_merge_build_repeat.chat_database_service.model.ChatMessageEntity;
import team_merge_build_repeat.chat_database_service.repository.ChatMessageRepository;

import java.time.Clock;
import java.util.List;
import java.util.UUID;

@Service
public class ChatService {
	private final ChatMessageRepository repository;
	private final Clock clock;

	public ChatService(ChatMessageRepository repository, Clock clock) {
		this.repository = repository;
		this.clock = clock;
	}

	@Transactional(readOnly = true)
	public ChatResponse getChat(UUID gameId) {
		List<ChatMessageResponse> messages = repository.findByGameId(gameId).stream()
				.map(this::toResponse)
				.toList();
		return new ChatResponse(gameId, messages);
	}

	@Transactional
	public ChatMessageResponse createMessage(UUID gameId, CreateChatMessageRequest request) {
		ChatMessageEntity entity = new ChatMessageEntity(
				UUID.randomUUID(),
				gameId,
				request.role(),
				request.content(),
				clock.instant()
		);

		ChatMessageEntity saved = repository.save(entity);
		saved.markPersisted();
		return toResponse(saved);
	}

	private ChatMessageResponse toResponse(ChatMessageEntity entity) {
		return new ChatMessageResponse(
				entity.getId(),
				entity.getGameId(),
				entity.getRole(),
				entity.getContent(),
				entity.getCreatedAt()
		);
	}
}
