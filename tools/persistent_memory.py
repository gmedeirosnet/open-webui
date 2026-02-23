"""
title: Persistent Memory Tool
author: Personal AI Agent
version: 2.0.0
description: Persistent key-value memory storage using SQLite
"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager


MEMORY_DB = "/app/backend/data/agent_memory.db"


class Tools:
    def __init__(self):
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(MEMORY_DB)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize the database schema."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

    def save_memory(self, key: str, value: str) -> str:
        """
        Saves information to persistent memory.

        :param key: Memory key/name
        :param value: Content to save
        :return: Confirmation message
        """
        try:
            timestamp = datetime.now().isoformat()

            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO memories (key, value, timestamp, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET
                        value = excluded.value,
                        updated_at = excluded.updated_at
                """, (key, value, timestamp, timestamp))

            return f"✓ Memory '{key}' saved successfully."

        except Exception as e:
            return f"Error saving memory: {str(e)}"

    def recall_memory(self, key: str) -> str:
        """
        Retrieves information from persistent memory.

        :param key: Memory key to retrieve
        :return: Stored value
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT value, timestamp, updated_at FROM memories WHERE key = ?",
                    (key,)
                )
                row = cursor.fetchone()

            if not row:
                return f"No memory found for '{key}'."

            updated_info = ""
            if row["updated_at"] != row["timestamp"]:
                updated_info = f"\nLast updated: {row['updated_at']}"

            return f"[Memory: {key}]\nStored: {row['timestamp']}{updated_info}\n\n{row['value']}"

        except Exception as e:
            return f"Error recalling memory: {str(e)}"

    def list_memories(self) -> str:
        """
        Lists all keys stored in persistent memory.

        :return: List of memory keys
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT key, timestamp, updated_at FROM memories ORDER BY key"
                )
                rows = cursor.fetchall()

            if not rows:
                return "Memory is empty."

            result = f"Stored memories ({len(rows)}):\n\n"

            for row in rows:
                if row["updated_at"] != row["timestamp"]:
                    result += f"• {row['key']} (saved: {row['timestamp']}, updated: {row['updated_at']})\n"
                else:
                    result += f"• {row['key']} (saved: {row['timestamp']})\n"

            return result

        except Exception as e:
            return f"Error listing memories: {str(e)}"

    def delete_memory(self, key: str) -> str:
        """
        Deletes a memory entry.

        :param key: Memory key to delete
        :return: Confirmation message
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("DELETE FROM memories WHERE key = ?", (key,))

                if cursor.rowcount == 0:
                    return f"No memory found for '{key}'."

            return f"✓ Memory '{key}' deleted successfully."

        except Exception as e:
            return f"Error deleting memory: {str(e)}"

    def search_memories(self, search_term: str) -> str:
        """
        Searches memory keys and values for a term.

        :param search_term: Term to search for
        :return: Matching memories
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT key, value, timestamp
                    FROM memories
                    WHERE key LIKE ? OR value LIKE ?
                    ORDER BY updated_at DESC
                """, (f"%{search_term}%", f"%{search_term}%"))
                rows = cursor.fetchall()

            if not rows:
                return f"No memories found matching '{search_term}'."

            result = f"Found {len(rows)} matching memories:\n\n"
            for row in rows:
                preview = row["value"][:100] + "..." if len(row["value"]) > 100 else row["value"]
                result += f"• {row['key']}\n  {preview}\n  (saved: {row['timestamp']})\n\n"

            return result

        except Exception as e:
            return f"Error searching memories: {str(e)}"
