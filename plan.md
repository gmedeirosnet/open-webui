Ótima combinação! Aqui está um guia completo para construires o teu agente pessoal local.

---

## Arquitetura Geral

```
Open WebUI  →  Ollama (LLM local)
                    ↕
              Agente Python (tools)
              ├── Pesquisa web (DuckDuckGo)
              ├── Leitura PDFs
              ├── Memória persistente (JSON/SQLite)
              └── Execução de código (subprocess)
```

O Open WebUI suporta **Functions/Tools** nativamente via um sistema de plugins em Python. É a forma mais limpa de integrar tudo sem frameworks externas.

---

## 1. Instalar o Open WebUI

```bash
pip install open-webui
open-webui serve
# Acede em http://localhost:8080
```

Nas definições do Open WebUI, aponta para o teu Ollama em `http://localhost:11434`.

---

## 2. Criar as Tools no Open WebUI

No Open WebUI vai a **Workspace → Tools → "+"** e cria cada tool como um ficheiro Python.

### 🔍 Tool: Pesquisa na Web

```python
import httpx

class Tools:
    def search_web(self, query: str) -> str:
        """
        Pesquisa na web usando DuckDuckGo.
        :param query: O termo a pesquisar
        :return: Resultados da pesquisa
        """
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1}
        r = httpx.get(url, params=params, timeout=10)
        data = r.json()
        results = []
        for item in data.get("RelatedTopics", [])[:5]:
            if "Text" in item:
                results.append(item["Text"])
        return "\n".join(results) if results else "Sem resultados."
```

---

### 📄 Tool: Leitura de PDFs

```bash
pip install pymupdf
```

```python
import fitz  # pymupdf
import os

class Tools:
    def read_pdf(self, filepath: str) -> str:
        """
        Lê o conteúdo de um ficheiro PDF local.
        :param filepath: Caminho absoluto para o PDF
        :return: Texto extraído do PDF
        """
        if not os.path.exists(filepath):
            return f"Ficheiro não encontrado: {filepath}"
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text[:4000]  # limita para não exceder contexto
```

---

### 🧠 Tool: Memória Persistente

```python
import json
import os

MEMORY_FILE = os.path.expanduser("~/.agent_memory.json")

class Tools:
    def save_memory(self, key: str, value: str) -> str:
        """
        Guarda uma informação na memória persistente.
        :param key: Nome/chave da memória
        :param value: Conteúdo a guardar
        :return: Confirmação
        """
        memory = self._load()
        memory[key] = value
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        return f"Memória '{key}' guardada."

    def recall_memory(self, key: str) -> str:
        """
        Recupera uma informação da memória persistente.
        :param key: Nome/chave a recuperar
        :return: Valor guardado
        """
        memory = self._load()
        return memory.get(key, f"Nenhuma memória encontrada para '{key}'.")

    def list_memories(self) -> str:
        """
        Lista todas as chaves guardadas na memória.
        :return: Lista de chaves
        """
        memory = self._load()
        keys = list(memory.keys())
        return "Memórias: " + ", ".join(keys) if keys else "Memória vazia."

    def _load(self) -> dict:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                return json.load(f)
        return {}
```

---

### ⚙️ Tool: Execução de Código Python

```python
import subprocess
import tempfile
import os

class Tools:
    def run_python(self, code: str) -> str:
        """
        Executa um bloco de código Python e devolve o output.
        :param code: Código Python a executar
        :return: stdout ou stderr da execução
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write(code)
            tmp_path = f.name
        try:
            result = subprocess.run(
                ["python3", tmp_path],
                capture_output=True, text=True, timeout=15
            )
            output = result.stdout or result.stderr
            return output[:2000]
        except subprocess.TimeoutExpired:
            return "Erro: timeout de 15 segundos excedido."
        finally:
            os.unlink(tmp_path)
```

---

## 3. Ativar as Tools no Modelo

No Open WebUI, ao iniciar uma conversa, clica no ícone **"Tools"** (⚙️) e ativa as tools que criaste. O modelo irá automaticamente decidir quando as invocar.

---

## 4. Escolher o Modelo Certo

Para que o agente use as tools corretamente, usa modelos com boa capacidade de **function calling**:

```bash
ollama pull llama3.1        # Boa opção geral
ollama pull qwen2.5         # Excelente para código
ollama pull mistral-nemo    # Leve e capaz
```

---

## 5. Dicas Importantes

**Segurança na execução de código** — considera isolar o `run_python` num ambiente virtual ou container Docker para evitar acesso ao sistema principal.

**Contexto dos PDFs** — se o PDF for muito longo, divide em chunks e guarda os mais relevantes na memória com `save_memory`.

**Pesquisa web mais rica** — podes trocar a DuckDuckGo API por SearXNG (também local) para resultados mais completos:
```bash
docker run -d -p 8888:8080 searxng/searxng
```
E depois aponta o `httpx.get` para `http://localhost:8888/search?q=...&format=json`.

---

Queres que detalhe alguma das tools, ou que mostre como encadear várias numa única chamada do agente?