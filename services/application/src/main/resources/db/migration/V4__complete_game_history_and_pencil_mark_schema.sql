UPDATE game_history
SET created_at = CURRENT_TIMESTAMP
WHERE created_at IS NULL;

ALTER TABLE game_history
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE pencil_mark_history
    ADD CONSTRAINT fk_pencil_mark_history_game
        FOREIGN KEY (game_id) REFERENCES game_properties (id) ON DELETE CASCADE;

CREATE INDEX idx_pencil_mark_history_game_id ON pencil_mark_history (game_id);
