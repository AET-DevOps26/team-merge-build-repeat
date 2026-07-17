package com.sudokuai.merge_build_repeat.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

 @ExceptionHandler(NoTemplateException.class)
 public ResponseEntity<Map<String, Object>> handleNoTemplate(NoTemplateException ex) {
 return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of(
 "timestamp", Instant.now().toString(),
 "status",404,
 "error", "Not Found",
 "message", ex.getMessage()
 ));
 }

 @ExceptionHandler(IllegalArgumentException.class)
 public ResponseEntity<Map<String, Object>> handleIllegalArgument(IllegalArgumentException ex) {
 return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of(
 "timestamp", Instant.now().toString(),
 "status",400,
 "error", "Bad Request",
 "message", ex.getMessage()
 ));
 }
}
