package team_merge_build_repeat.chat_database_service.repository;

import org.springframework.data.jdbc.repository.query.Query;
import org.springframework.data.repository.CrudRepository;
import team_merge_build_repeat.chat_database_service.model.ChatMessageEntity;

import java.util.List;
import java.util.UUID;

public interface ChatMessageRepository extends CrudRepository<ChatMessageEntity, UUID> {

	@Query("""
			SELECT "id", "game_id", "role", "content", "created_at"
			FROM "chat_messages"
			WHERE "game_id" = :gameId
			ORDER BY "created_at" ASC, "id" ASC
			""")
	List<ChatMessageEntity> findByGameId(UUID gameId);
}
