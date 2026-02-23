"""
title: Persistent Memory Tool
author: Personal AI Agent
version: 1.0.0
description: Persistent key-value memory storage for the agent
"""

import json
import os
from datetime import datetime


MEMORY_FILE = "/app/backend/data/agent_memory.json"


class Tools:
    def __init__(self):
        pass

    def save_memory(self, key: str, value: str) -> str:
        """
        Saves information to persistent memory.

        :param key: Memory key/name
        :param value: Content to save
        :return: Confirmation message
        """
        try:
            memory = self._load()
            memory[key] = {
                "value": value,
                "timestamp": datetime.now().isoformat()
            }

            with open(MEMORY_FILE, "w") as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)

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
            memory = self._load()

            if key not in memory:
                return f"No memory found for '{key}'."

            entry = memory[key]
            value = entry.get("value", entry) if isinstance(entry, dict) else entry
            timestamp = entry.get("timestamp", "unknown") if isinstance(entry, dict) else "unknown"

            return f"[Memory: {key}]\nStored: {timestamp}\n\n{value}"

        except Exception as e:
            return f"Error recalling memory: {str(e)}"

    def list_memories(self) -> str:
        """
        Lists all keys stored in persistent memory.

        :return: List of memory keys
        """
        try:
            memory = self._load()

            if not memory:
                return "Memory is empty."

            keys = list(memory.keys())
            result = f"Stored memories ({len(keys)}):\n\n"

            for key in sorted(keys):
                entry = memory[key]
                timestamp = entry.get("timestamp", "unknown") if isinstance(entry, dict) else "unknown"
                result += f"• {key} (saved: {timestamp})\n"

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
            memory = self._load()

            if key not in memory:
                return f"No memory found for '{key}'."

            del memory[key]

            with open(MEMORY_FILE, "w") as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)

            return f"✓ Memory '{key}' deleted successfully."

        except Exception as e:
            return f"Error deleting memory: {str(e)}"

    def _load(self) -> dict:
        """Load memory from file."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
