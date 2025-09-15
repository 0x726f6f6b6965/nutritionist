CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    line_id TEXT UNIQUE,
    height NUMERIC(10, 2),
    weight NUMERIC(10, 2),
    age INTEGER,
    gender SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS histories (
    id BIGSERIAL PRIMARY KEY,
    line_id TEXT,
    meal SMALLINT,
    description TEXT,
    photo BYTEA,
    calories_kcal BIGINT,
    protein_g BIGINT,
    carbs_g BIGINT,
    fat_g BIGINT,
    sodium_mg BIGINT,
    ai_description TEXT,
    ai_suggest TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_histories_line_id FOREIGN KEY (line_id) REFERENCES users(line_id) ON DELETE CASCADE
);
