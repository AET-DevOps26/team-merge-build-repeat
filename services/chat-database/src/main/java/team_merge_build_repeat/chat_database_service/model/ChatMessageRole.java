package team_merge_build_repeat.chat_database_service.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

import java.util.Locale;

public enum ChatMessageRole {
	USER("user"),
	ASSISTANT("assistant");

	private final String value;

	ChatMessageRole(String value) {
		this.value = value;
	}

	@JsonValue
	public String value() {
		return value;
	}

	@JsonCreator
	public static ChatMessageRole fromValue(String value) {
		if (value == null) {
			return null;
		}

		return switch (value.toLowerCase(Locale.ROOT)) {
			case "user" -> USER;
			case "assistant" -> ASSISTANT;
			default -> throw new IllegalArgumentException("Unsupported chat message role: " + value);
		};
	}
}
