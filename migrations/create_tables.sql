-- Recria as tabelas do banco de dados

-- Tabela de participantes
DROP TABLE IF EXISTS participant_event CASCADE;
DROP TABLE IF EXISTS participant_meeting CASCADE;
DROP TABLE IF EXISTS participant CASCADE;
DROP TABLE IF EXISTS meeting CASCADE;
DROP TABLE IF EXISTS event CASCADE;
DROP TABLE IF EXISTS attendance CASCADE;

CREATE TABLE participant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(100),
    check_in_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    theme VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meeting (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE participant_event (
    participant_id INTEGER REFERENCES participant(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES event(id) ON DELETE CASCADE,
    PRIMARY KEY (participant_id, event_id)
);

CREATE TABLE participant_meeting (
    participant_id INTEGER REFERENCES participant(id) ON DELETE CASCADE,
    meeting_id INTEGER REFERENCES meeting(id) ON DELETE CASCADE,
    PRIMARY KEY (participant_id, meeting_id)
);

-- Tabela attendance para registrar presença em encontros
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL REFERENCES meeting(id) ON DELETE CASCADE,
    participant_id INTEGER NOT NULL REFERENCES participant(id) ON DELETE CASCADE,
    present BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(meeting_id, participant_id)
);
