# Open WebUI Local Agent - Setup Instructions

## 📁 Project Structure

```
open-webui/
├── Dockerfile              # Custom Open WebUI image with tools
├── docker-compose.yml      # Docker Compose configuration
├── tools/                  # AI Agent tools
│   ├── search_web.py       # Web search (DuckDuckGo)
│   ├── read_pdf.py         # PDF reader
│   └── persistent_memory.py # SQLite-based memory storage
├── plan.md                 # Original plan (Portuguese)
└── history.md              # Development history log
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ollama running on host machine (port 11434)
- QWEN3:latest model installed in Ollama

### 1. Build and Start

```bash
docker-compose up -d --build
```

This will:
- Build a custom Open WebUI image with tools
- Install dependencies (httpx, pymupdf)
- Copy all tools to the container
- Start Open WebUI on http://localhost:3000

### 2. Access Open WebUI

Open your browser and navigate to:
```
http://localhost:3000
```

### 3. Enable Tools

In Open WebUI:
1. Start a new chat
2. Click the **Tools** icon (⚙️) in the chat interface
3. Enable the tools you want to use:
   - **Web Search Tool** - Search the internet
   - **PDF Reader Tool** - Read PDF files
   - **Persistent Memory Tool** - Save and recall information

### 4. Test the Tools

Try these example prompts:

**Web Search:**
```
Search the web for "Python best practices 2026"
```

**PDF Reading:**
```
Read the PDF file at /path/to/document.pdf
```

**Memory:**
```
Save to memory: key="project_name" value="Open WebUI Agent"
Recall memory: key="project_name"
List all memories
```

## 📋 Available Tools

### 🔍 Web Search Tool
- **Function:** `search_web(query: str)`
- **Description:** Searches DuckDuckGo and returns top results
- **Usage:** Automatically invoked when you ask to search the web

### 📄 PDF Reader Tool
- **Function:** `read_pdf(filepath: str)`
- **Description:** Extracts text from PDF files (up to 8000 chars)
- **Usage:** Provide absolute path to PDF file
- **Note:** For Docker usage, mount volumes with PDFs

### 🧠 Persistent Memory Tool
- **Functions:**
  - `save_memory(key: str, value: str)` - Save information
  - `recall_memory(key: str)` - Retrieve information
  - `list_memories()` - List all saved keys
  - `delete_memory(key: str)` - Delete a memory entry
  - `search_memories(search_term: str)` - Search keys and values
- **Storage:** SQLite database at `/app/backend/data/agent_memory.db`
- **Features:**
  - ACID-compliant transactions
  - Automatic timestamp tracking (created and updated)
  - Full-text search capabilities
  - Indexed queries for fast lookups
- **Persistence:** Data persists across container restarts

## 🛠️ Management Commands

### View logs
```bash
docker-compose logs -f
```

### Stop the service
```bash
docker-compose down
```

### Restart after changes
```bash
docker-compose down
docker-compose up -d --build
```

### Access container shell
```bash
docker exec -it open-webui /bin/bash
```

## 📂 Using PDFs

To read PDFs from your host machine, mount a volume in `docker-compose.yml`:

```yaml
volumes:
  - open-webui-data:/app/backend/data
  - ./pdfs:/pdfs  # Add this line
```

Then restart:
```bash
docker-compose down
docker-compose up -d --build
```

Now you can read PDFs with: `Read /pdfs/document.pdf`

## 🔧 Configuration

### Environment Variables (in docker-compose.yml)

- `OLLAMA_BASE_URL` - Ollama server URL (default: http://host.docker.internal:11434)
- `WEBUI_AUTH` - Enable authentication (true/false)
- `WEBUI_NAME` - Custom name for the interface

### Recommended Ollama Models

For best tool usage:
```bash
ollama pull llama3.1        # Good general purpose
ollama pull qwen2.5         # Excellent for code
ollama pull mistral-nemo    # Lightweight
```

## 🐛 Troubleshooting

### Tools not appearing
1. Check logs: `docker-compose logs -f`
2. Verify tools are copied: `docker exec -it open-webui ls /app/backend/data/tools/`
3. Rebuild: `docker-compose up -d --build`

### Can't connect to Ollama
1. Verify Ollama is running: `ollama list`
2. Check Ollama URL in docker-compose.yml
3. Test connectivity: `docker exec -it open-webui curl http://host.docker.internal:11434`

### PDF reading fails
1. Verify file path is absolute
2. Check file exists and is readable
3. Mount the directory containing PDFs as a volume

## 📝 Next Steps

- Add more tools (file operations, calendar, etc.)
- Implement code execution tool with sandboxing
- Add RAG capabilities with vector database
- Integrate SearXNG for enhanced web search

---

**Built with:**
- [Open WebUI](https://github.com/open-webui/open-webui)
- [Ollama](https://ollama.ai/)
- Docker & Docker Compose
