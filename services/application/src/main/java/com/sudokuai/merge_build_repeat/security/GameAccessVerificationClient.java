package com.sudokuai.merge_build_repeat.security;

import java.util.UUID;

public interface GameAccessVerificationClient {
	GameAccessVerificationResult verify(UUID userId, UUID gameId);
}
