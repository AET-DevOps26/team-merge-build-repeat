package com.sudokuai.merge_build_repeat.security;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.bind.DefaultValue;

import java.time.Duration;

@ConfigurationProperties(prefix = "application-service.verify")
public record ApplicationServiceVerificationProperties(
		@DefaultValue("http://application:8080") String baseUrl,
		@DefaultValue("1s") Duration connectTimeout,
		@DefaultValue("2s") Duration readTimeout
) {
}
