package team_merge_build_repeat.chat_database_service.dto;

import java.time.Instant;

public record ErrorResponse(
		int status,
		String error,
		String message,
		String path,
		Instant timestamp
) {
}
