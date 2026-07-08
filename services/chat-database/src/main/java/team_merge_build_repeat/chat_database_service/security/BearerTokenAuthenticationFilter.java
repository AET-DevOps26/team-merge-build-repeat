package team_merge_build_repeat.chat_database_service.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

public class BearerTokenAuthenticationFilter extends OncePerRequestFilter {
	@Override
	protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
			throws ServletException, IOException {
		String authorization = request.getHeader("Authorization");
		if (authorization != null && authorization.startsWith("Bearer ")) {
			String bearerToken = authorization.substring(7).trim();
			if (!bearerToken.isEmpty()) {
				SecurityContextHolder.getContext().setAuthentication(
						UsernamePasswordAuthenticationToken.authenticated(bearerToken, null, List.of()));
			}
		}

		filterChain.doFilter(request, response);
	}
}
