package team_merge_build_repeat.chat_database_service.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import team_merge_build_repeat.chat_database_service.security.SecurityErrorResponseWriter;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfiguration {
	@Bean
	SecurityFilterChain securityFilterChain(
			HttpSecurity http,
			SecurityErrorResponseWriter securityErrorResponseWriter
	) throws Exception {
		return http
				.csrf(csrf -> csrf.disable())
				.authorizeHttpRequests(authorize -> authorize
						.requestMatchers("/v1/chat/**").authenticated()
						.anyRequest().permitAll())
				.oauth2ResourceServer(oauth2 -> oauth2
						.jwt(Customizer.withDefaults())
						.authenticationEntryPoint(securityErrorResponseWriter))
				.exceptionHandling(exceptions -> exceptions
						.authenticationEntryPoint(securityErrorResponseWriter)
						.accessDeniedHandler(securityErrorResponseWriter))
				.build();
	}
}
