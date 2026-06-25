package team_merge_build_repeat.chat_database_service.exception;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolationException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import team_merge_build_repeat.chat_database_service.dto.ErrorResponse;
import team_merge_build_repeat.chat_database_service.security.GameVerificationUnavailableException;

import java.time.Clock;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.stream.Collectors;

@RestControllerAdvice
public class ApiExceptionHandler {
	private final Clock clock;

	public ApiExceptionHandler(Clock clock) {
		this.clock = clock;
	}

	@ExceptionHandler(UnauthorizedException.class)
	public ResponseEntity<ErrorResponse> handleUnauthorized(UnauthorizedException exception, HttpServletRequest request) {
		return build(HttpStatus.UNAUTHORIZED, exception.getMessage(), request);
	}

	@ExceptionHandler(ForbiddenException.class)
	public ResponseEntity<ErrorResponse> handleForbidden(ForbiddenException exception, HttpServletRequest request) {
		return build(HttpStatus.FORBIDDEN, exception.getMessage(), request);
	}

	@ExceptionHandler(GameVerificationUnavailableException.class)
	public ResponseEntity<ErrorResponse> handleVerificationUnavailable(GameVerificationUnavailableException exception, HttpServletRequest request) {
		return build(HttpStatus.SERVICE_UNAVAILABLE, "Game access verification is temporarily unavailable.", request);
	}

	@ExceptionHandler({
			MethodArgumentNotValidException.class,
			ConstraintViolationException.class,
			HttpMessageNotReadableException.class,
			MethodArgumentTypeMismatchException.class,
			IllegalArgumentException.class
	})
	public ResponseEntity<ErrorResponse> handleBadRequest(Exception exception, HttpServletRequest request) {
		return build(HttpStatus.BAD_REQUEST, extractMessage(exception), request);
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<ErrorResponse> handleUnexpected(Exception exception, HttpServletRequest request) {
		return build(HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected server error occurred.", request);
	}

	private ResponseEntity<ErrorResponse> build(HttpStatus status, String message, HttpServletRequest request) {
		ErrorResponse body = new ErrorResponse(status.value(), status.getReasonPhrase(), message, request.getRequestURI(), Instant.now(clock));
		return ResponseEntity.status(status).body(body);
	}

	private String extractMessage(Exception exception) {
		if (exception instanceof MethodArgumentNotValidException methodArgumentNotValidException) {
			Set<String> messages = new LinkedHashSet<>();
			for (FieldError fieldError : methodArgumentNotValidException.getBindingResult().getFieldErrors()) {
				messages.add(fieldError.getField() + " " + fieldError.getDefaultMessage());
			}
			return messages.stream().collect(Collectors.joining(", "));
		}

		if (exception instanceof ConstraintViolationException constraintViolationException) {
			return constraintViolationException.getConstraintViolations().stream()
					.map(violation -> violation.getPropertyPath() + " " + violation.getMessage())
					.collect(Collectors.joining(", "));
		}

		return exception.getMessage() == null || exception.getMessage().isBlank()
				? "The request is invalid."
				: exception.getMessage();
	}
}
