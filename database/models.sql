CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    username TEXT REFERENCES users(username),
    role TEXT NOT NULL,           -- 'user' or 'assistant'
    message TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);