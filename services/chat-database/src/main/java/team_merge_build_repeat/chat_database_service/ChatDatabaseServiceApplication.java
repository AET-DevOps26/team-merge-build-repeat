package team_merge_build_repeat.chat_database_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.time.Clock;

@SpringBootApplication
public class ChatDatabaseServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(ChatDatabaseServiceApplication.class, args);
	}

	@Bean
	Clock clock() {
		return Clock.systemUTC();
	}

}
