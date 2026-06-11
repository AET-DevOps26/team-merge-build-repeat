package team_merge_build_repeat.chat_database_service.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import team_merge_build_repeat.chat_database_service.model.ChatMessageRole;

public record CreateChatMessageRequest(
		@NotNull ChatMessageRole role,
		@NotBlank @Size(min = 1, max = 10000) String content
) {
}
