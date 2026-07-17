ALTER TABLE game_properties
    ADD COLUMN user_id UUID;

ALTER TABLE game_history
    ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE pencil_mark_history (
    id UUID NOT NULL,
    game_id UUID NOT NULL,
    row INTEGER NOT NULL,
    col INTEGER NOT NULL,
    value INTEGER NOT NULL,
    action VARCHAR(255) NOT NULL,
    initial BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT pk_pencil_mark_history PRIMARY KEY (id),
    CONSTRAINT fk_pencil_mark_history_game
        FOREIGN KEY (game_id) REFERENCES game_properties (id) ON DELETE CASCADE
);

CREATE INDEX idx_pencil_mark_history_game_id ON pencil_mark_history (game_id);
