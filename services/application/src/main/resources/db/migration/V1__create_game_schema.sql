CREATE TABLE account (
    user_id UUID NOT NULL,
    game_id UUID,
    CONSTRAINT pk_account PRIMARY KEY (user_id)
);

CREATE TABLE game_history (
    id UUID NOT NULL,
    game_id UUID NOT NULL,
    row INTEGER NOT NULL,
    col INTEGER NOT NULL,
    value INTEGER NOT NULL,
    CONSTRAINT pk_game_history PRIMARY KEY (id)
);

CREATE TABLE game_properties (
    id UUID NOT NULL,
    template_id UUID NOT NULL,
    current_state VARCHAR(255) NOT NULL,
    CONSTRAINT pk_game_properties PRIMARY KEY (id)
);

CREATE TABLE game_template (
    id UUID NOT NULL,
    difficulty VARCHAR(255) NOT NULL,
    template_data VARCHAR(255) NOT NULL,
    solution_data VARCHAR(255) NOT NULL,
    CONSTRAINT pk_game_template PRIMARY KEY (id)
);

CREATE TABLE pencil_marks (
    id UUID NOT NULL,
    game_id UUID,
    row INTEGER NOT NULL,
    col INTEGER NOT NULL,
    marks VARCHAR(255),
    version BIGINT,
    CONSTRAINT pk_pencil_marks PRIMARY KEY (id)
);
