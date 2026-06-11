package team_merge_build_repeat.chat_database_service.dto;

import java.util.List;
import java.util.UUID;

public record ChatResponse(
		UUID gameId,
		List<ChatMessageResponse> messages
) {
}
