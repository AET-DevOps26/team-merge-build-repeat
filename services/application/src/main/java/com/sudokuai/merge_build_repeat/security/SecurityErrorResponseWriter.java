package com.sudokuai.merge_build_repeat.security;

import com.sudokuai.merge_build_repeat.dto.ErrorResponse;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;
import tools.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.time.Clock;
import java.time.Instant;

@Component
public class SecurityErrorResponseWriter implements AuthenticationEntryPoint, AccessDeniedHandler {
	private final ObjectMapper objectMapper;

	public SecurityErrorResponseWriter(ObjectMapper objectMapper) {
		this.objectMapper = objectMapper;
	}

	@Override
	public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException {
		write(response, request, HttpStatus.UNAUTHORIZED, "Authentication is required or the provided token is invalid.");
	}

	@Override
	public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException exception) throws IOException {
		write(response, request, HttpStatus.FORBIDDEN, "The authenticated user is not allowed to access this game chat.");
	}

	private void write(HttpServletResponse response, HttpServletRequest request, HttpStatus status, String message) throws IOException {
		response.setStatus(status.value());
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		objectMapper.writeValue(response.getOutputStream(), new ErrorResponse(
				status.value(), status.getReasonPhrase(), message, request.getRequestURI(), Instant.now()));
	}

}
