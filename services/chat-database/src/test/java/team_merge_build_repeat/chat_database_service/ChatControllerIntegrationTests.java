package team_merge_build_repeat.chat_database_service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicLong;

import team_merge_build_repeat.chat_database_service.security.GameAccessVerificationClient;
import team_merge_build_repeat.chat_database_service.security.GameAccessVerificationResult;
import team_merge_build_repeat.chat_database_service.security.GameVerificationUnavailableException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
class ChatControllerIntegrationTests {
	private static final UUID TEST_USER_ID = UUID.fromString("00000000-0000-0000-0000-000000000001");
	private static final UUID FORBIDDEN_USER_ID = UUID.fromString("00000000-0000-0000-0000-000000000002");
	private static final UUID INVALID_USER_ID = UUID.fromString("00000000-0000-0000-0000-000000000003");
	private static final UUID UNAVAILABLE_USER_ID = UUID.fromString("00000000-0000-0000-0000-000000000004");

	@Autowired
	private WebApplicationContext context;

	private MockMvc mockMvc;

	private static org.springframework.test.web.servlet.request.RequestPostProcessor jwtForUser(UUID userId) {
		return jwt().jwt(jwt -> jwt.subject(userId.toString()));
	}

	@BeforeEach
	void setUp() {
		mockMvc = MockMvcBuilders.webAppContextSetup(context).apply(springSecurity()).build();
	}

	@TestConfiguration
	static class TestClockConfiguration {
		@Bean
		@Primary
		Clock testClock() {
			AtomicLong counter = new AtomicLong();
			return new Clock() {
				@Override
				public ZoneOffset getZone() {
					return ZoneOffset.UTC;
				}

				@Override
				public Clock withZone(java.time.ZoneId zone) {
					return this;
				}

				@Override
				public Instant instant() {
					return Instant.parse("2026-01-01T00:00:00Z").plusMillis(counter.getAndIncrement());
				}
			};
		}

		@Bean
		@Primary
		GameAccessVerificationClient gameAccessVerificationClient() {
			return (userId, gameId, authorization) -> {
				if (TEST_USER_ID.equals(userId)) {
					return GameAccessVerificationResult.ALLOWED;
				}
				if (FORBIDDEN_USER_ID.equals(userId)) {
					return GameAccessVerificationResult.FORBIDDEN;
				}
				if (INVALID_USER_ID.equals(userId)) {
					return GameAccessVerificationResult.UNAUTHORIZED;
				}
				if (UNAVAILABLE_USER_ID.equals(userId)) {
					throw new GameVerificationUnavailableException("unavailable", null);
				}
				return GameAccessVerificationResult.UNAUTHORIZED;
			};
		}
	}

	@Test
	void getChatReturnsEmptyChatForNewGame() throws Exception {
		UUID gameId = UUID.randomUUID();

		mockMvc.perform(get("/v1/chat/{gameId}", gameId)
						.with(jwtForUser(TEST_USER_ID)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.gameId").value(gameId.toString()))
				.andExpect(jsonPath("$.messages").isArray())
				.andExpect(jsonPath("$.messages").isEmpty());
	}

	@Test
	void createMessageStoresAndReturnsMessage() throws Exception {
		UUID gameId = UUID.randomUUID();

		MvcResult result = mockMvc.perform(post("/v1/chat/{gameId}/messages", gameId)
						.with(jwtForUser(TEST_USER_ID))
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"role":"user","content":"Need a hint"}
								"""))
				.andExpect(status().isCreated())
				.andExpect(header().string("Location", "/v1/chat/" + gameId))
				.andExpect(jsonPath("$.gameId").value(gameId.toString()))
				.andExpect(jsonPath("$.role").value("user"))
				.andExpect(jsonPath("$.content").value("Need a hint"))
				.andExpect(jsonPath("$.id").isNotEmpty())
				.andExpect(jsonPath("$.createdAt").isNotEmpty())
				.andReturn();

		mockMvc.perform(get("/v1/chat/{gameId}", gameId)
						.with(jwtForUser(TEST_USER_ID)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.messages.length()").value(1))
				.andExpect(jsonPath("$.messages[0].content").value("Need a hint"));

		assertThat(result.getResponse().getContentAsString()).contains("Need a hint");
	}

	@Test
	void getChatWithoutAuthorizationReturnsUnauthorized() throws Exception {
		mockMvc.perform(get("/v1/chat/{gameId}", UUID.randomUUID()))
				.andExpect(status().isUnauthorized())
				.andExpect(jsonPath("$.status").value(401))
				.andExpect(jsonPath("$.error").value("Unauthorized"));
	}

	@Test
	void getChatForForbiddenGameReturnsForbidden() throws Exception {
		mockMvc.perform(get("/v1/chat/{gameId}", UUID.randomUUID())
						.with(jwtForUser(FORBIDDEN_USER_ID)))
				.andExpect(status().isForbidden())
				.andExpect(jsonPath("$.status").value(403));
	}

	@Test
	void forbiddenMessageCreationDoesNotStoreAMessage() throws Exception {
		UUID gameId = UUID.randomUUID();

		mockMvc.perform(post("/v1/chat/{gameId}/messages", gameId)
						.with(jwtForUser(FORBIDDEN_USER_ID))
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"role":"user","content":"Should not be stored"}
								"""))
				.andExpect(status().isForbidden());

		mockMvc.perform(get("/v1/chat/{gameId}", gameId)
						.with(jwtForUser(TEST_USER_ID)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.messages").isEmpty());
	}

	@Test
	void getChatWithInvalidTokenReturnsUnauthorized() throws Exception {
		mockMvc.perform(get("/v1/chat/{gameId}", UUID.randomUUID())
						.with(jwtForUser(INVALID_USER_ID)))
				.andExpect(status().isUnauthorized())
				.andExpect(jsonPath("$.status").value(401));
	}

	@Test
	void getChatWhenVerificationIsUnavailableReturnsServiceUnavailable() throws Exception {
		mockMvc.perform(get("/v1/chat/{gameId}", UUID.randomUUID())
						.with(jwtForUser(UNAVAILABLE_USER_ID)))
				.andExpect(status().isServiceUnavailable())
				.andExpect(jsonPath("$.status").value(503));
	}

	@Test
	void invalidRequestBodyReturnsBadRequest() throws Exception {
		mockMvc.perform(post("/v1/chat/{gameId}/messages", UUID.randomUUID())
						.with(jwtForUser(TEST_USER_ID))
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"role":"user","content":""}
								"""))
				.andExpect(status().isBadRequest())
				.andExpect(jsonPath("$.status").value(400));
	}

	@Test
	void messagesAreReturnedChronologically() throws Exception {
		UUID gameId = UUID.randomUUID();

		mockMvc.perform(post("/v1/chat/{gameId}/messages", gameId)
						.with(jwtForUser(TEST_USER_ID))
				.contentType(MediaType.APPLICATION_JSON)
				.content("""
								{"role":"user","content":"First"}
								"""))
				.andExpect(status().isCreated());

		mockMvc.perform(post("/v1/chat/{gameId}/messages", gameId)
						.with(jwtForUser(TEST_USER_ID))
				.contentType(MediaType.APPLICATION_JSON)
				.content("""
								{"role":"assistant","content":"Second"}
								"""))
				.andExpect(status().isCreated());

		mockMvc.perform(get("/v1/chat/{gameId}", gameId)
						.with(jwtForUser(TEST_USER_ID)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.messages[0].content").value("First"))
				.andExpect(jsonPath("$.messages[1].content").value("Second"));
	}
}
