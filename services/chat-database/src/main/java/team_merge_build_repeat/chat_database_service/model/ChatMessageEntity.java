package team_merge_build_repeat.chat_database_service.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.domain.Persistable;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import java.time.Instant;
import java.util.UUID;

@Table("chat_messages")
public class ChatMessageEntity implements Persistable<UUID> {
	@Id
	@Column("id")
	private UUID id;

	@Column("game_id")
	private UUID gameId;

	@Column("role")
	private ChatMessageRole role;

	@Column("content")
	private String content;

	@Column("created_at")
	private Instant createdAt;

	@Transient
	private boolean newEntity = true;

	public ChatMessageEntity() {
	}

	public ChatMessageEntity(UUID id, UUID gameId, ChatMessageRole role, String content, Instant createdAt) {
		this.id = id;
		this.gameId = gameId;
		this.role = role;
		this.content = content;
		this.createdAt = createdAt;
	}

	public void setId(UUID id) {
		this.id = id;
	}

	public UUID getGameId() {
		return gameId;
	}

	public void setGameId(UUID gameId) {
		this.gameId = gameId;
	}

	public ChatMessageRole getRole() {
		return role;
	}

	public void setRole(ChatMessageRole role) {
		this.role = role;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(Instant createdAt) {
		this.createdAt = createdAt;
	}

	@Override
	public UUID getId() {
		return id;
	}

	@Override
	public boolean isNew() {
		return newEntity;
	}

	public void markPersisted() {
		this.newEntity = false;
	}
}
