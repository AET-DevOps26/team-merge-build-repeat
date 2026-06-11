package team_merge_build_repeat.chat_database_service.dto;

import team_merge_build_repeat.chat_database_service.model.ChatMessageRole;

import java.time.Instant;
import java.util.UUID;

public record ChatMessageResponse(
		UUID id,
		UUID gameId,
		ChatMessageRole role,
		String content,
		Instant createdAt
) {
}
