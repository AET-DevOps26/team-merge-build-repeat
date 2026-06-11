package team_merge_build_repeat.chat_database_service.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import team_merge_build_repeat.chat_database_service.interceptor.BearerAuthInterceptor;

@Configuration
public class ChatWebConfiguration implements WebMvcConfigurer {
	private final BearerAuthInterceptor bearerAuthInterceptor;

	public ChatWebConfiguration(BearerAuthInterceptor bearerAuthInterceptor) {
		this.bearerAuthInterceptor = bearerAuthInterceptor;
	}

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(bearerAuthInterceptor)
				.addPathPatterns("/v1/chat/**");
	}
}
