CREATE TABLE "chat_messages" (
    "id" UUID PRIMARY KEY,
    "game_id" UUID NOT NULL,
    "role" VARCHAR(32) NOT NULL,
    "content" VARCHAR(10000) NOT NULL,
    "created_at" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT chat_messages_role_check CHECK ("role" IN ('user', 'assistant'))
);

CREATE INDEX chat_messages_game_id_created_at_id_idx
    ON "chat_messages" ("game_id", "created_at", "id");
