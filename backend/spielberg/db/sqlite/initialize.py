import sqlite3

# SQL to create the sessions table
CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    video_id TEXT,
    collection_id TEXT,
    created_at INTEGER,
    updated_at INTEGER,
    metadata JSON
)
"""

# SQL to create the conversations table
CREATE_CONVERSATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS conversations (
    session_id TEXT,
    conv_id TEXT,
    msg_id TEXT PRIMARY KEY,
    msg_type TEXT,
    agents JSON,
    actions JSON,
    content JSON,
    status TEXT,
    created_at INTEGER,
    updated_at INTEGER,
    metadata JSON,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
"""

# SQL to create the context_messages table
CREATE_CONTEXT_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS context_messages (
    session_id TEXT PRIMARY KEY,
    context_data JSON,
    created_at INTEGER,
    updated_at INTEGER,
    metadata JSON,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
"""

conn = sqlite3.connect("spielberg.db")

cursor = conn.cursor()

cursor.execute(CREATE_SESSIONS_TABLE)
cursor.execute(CREATE_CONVERSATIONS_TABLE)
cursor.execute(CREATE_CONTEXT_MESSAGES_TABLE)

conn.commit()
conn.close()
