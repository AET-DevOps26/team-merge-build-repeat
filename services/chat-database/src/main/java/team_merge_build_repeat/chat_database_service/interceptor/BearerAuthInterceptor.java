package team_merge_build_repeat.chat_database_service.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import team_merge_build_repeat.chat_database_service.exception.UnauthorizedException;

@Component
public class BearerAuthInterceptor implements HandlerInterceptor {
	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
		String authorization = request.getHeader("Authorization");
		if (authorization == null || !authorization.startsWith("Bearer ") || authorization.substring(7).isBlank()) {
			throw new UnauthorizedException("Authentication is required or the provided token is invalid.");
		}
		return true;
	}
}
