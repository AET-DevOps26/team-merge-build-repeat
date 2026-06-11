package team_merge_build_repeat.chat_database_service.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.convert.ReadingConverter;
import org.springframework.data.convert.WritingConverter;
import org.springframework.data.jdbc.core.convert.JdbcCustomConversions;
import team_merge_build_repeat.chat_database_service.model.ChatMessageRole;

import java.util.List;

@Configuration
public class JdbcConversionConfiguration {
	@Bean
	JdbcCustomConversions jdbcCustomConversions() {
		return new JdbcCustomConversions(List.of(
				new ChatMessageRoleToStringConverter(),
				new StringToChatMessageRoleConverter()
		));
	}

	@WritingConverter
	static class ChatMessageRoleToStringConverter implements Converter<ChatMessageRole, String> {
		@Override
		public String convert(ChatMessageRole source) {
			return source == null ? null : source.value();
		}
	}

	@ReadingConverter
	static class StringToChatMessageRoleConverter implements Converter<String, ChatMessageRole> {
		@Override
		public ChatMessageRole convert(String source) {
			return ChatMessageRole.fromValue(source);
		}
	}
}
