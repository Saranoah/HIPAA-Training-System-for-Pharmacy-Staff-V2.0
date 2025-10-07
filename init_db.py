#!/usr/bin/env python3
"""
Initialize PostgreSQL database for HIPAA Training System
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def init_database():
    """Initialize database schema"""
    try:
        conn = psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
        with conn:
            with conn.cursor() as cur:
                # Users table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id VARCHAR(100) PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role VARCHAR(50) NOT NULL,
                        facility VARCHAR(200) NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                ''')

                # Progress table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS progress (
                        user_id VARCHAR(100) NOT NULL,
                        lesson_id VARCHAR(100),
                        completed BOOLEAN DEFAULT FALSE,
                        quiz_score FLOAT,
                        quiz_taken BOOLEAN DEFAULT FALSE,
                        checklist_item_id INTEGER,
                        checklist_completed BOOLEAN DEFAULT FALSE,
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        PRIMARY KEY (user_id, lesson_id, checklist_item_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                ''')

                # Create indexes
                cur.execute('''
                    CREATE INDEX IF NOT EXISTS idx_progress_user
                    ON progress(user_id)
                ''')

        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    init_database()
