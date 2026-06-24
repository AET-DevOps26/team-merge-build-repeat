package team_merge_build_repeat.chat_database_service.controller;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import team_merge_build_repeat.chat_database_service.dto.ChatMessageResponse;
import team_merge_build_repeat.chat_database_service.dto.ChatResponse;
import team_merge_build_repeat.chat_database_service.dto.CreateChatMessageRequest;
import team_merge_build_repeat.chat_database_service.service.ChatService;

import java.net.URI;
import java.util.UUID;

@RestController
@RequestMapping("/v1")
public class ChatController {
	private final ChatService chatService;

	public ChatController(ChatService chatService) {
		this.chatService = chatService;
	}

	@GetMapping("/chat/{gameId}")
	@PreAuthorize("@gameAccessAuthorizer.hasAccess(authentication, #p0)")
	public ChatResponse getGameChat(@PathVariable UUID gameId) {
		return chatService.getChat(gameId);
	}

	@PostMapping("/chat/{gameId}/messages")
	@PreAuthorize("@gameAccessAuthorizer.hasAccess(authentication, #p0)")
	public ResponseEntity<ChatMessageResponse> createGameChatMessage(
			@PathVariable UUID gameId,
			@Valid @RequestBody CreateChatMessageRequest request
	) {
		ChatMessageResponse response = chatService.createMessage(gameId, request);
		return ResponseEntity.created(URI.create("/v1/chat/" + gameId)).body(response);
	}
}
