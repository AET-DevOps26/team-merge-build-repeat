ALTER TABLE game_properties
    ADD COLUMN user_id UUID;

ALTER TABLE game_history
    ADD COLUMN created_at TIMESTAMP WITH TIME ZONE;

CREATE TABLE pencil_mark_history (
    id UUID NOT NULL,
    game_id UUID NOT NULL,
    row INTEGER NOT NULL,
    col INTEGER NOT NULL,
    value INTEGER NOT NULL,
    action VARCHAR(255) NOT NULL,
    initial BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT pk_pencil_mark_history PRIMARY KEY (id)
);
