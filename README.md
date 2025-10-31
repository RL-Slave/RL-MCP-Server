# Ollama MCP Server

A complete Model Context Protocol (MCP) Server for Ollama with **28 tools**, enabling the use of Ollama models via the MCP protocol.

## Features

- ✅ **28 complete tools** for all Ollama functions
- ✅ **Streaming support** for chat and text generation
- ✅ **Model management** (Pull, Delete, Copy, Create, Update)
- ✅ **Embedding generation** (Single & Batch)
- ✅ **Context management** for multi-turn conversations
- ✅ **Batch operations** for efficient processing
- ✅ **System monitoring** and health checks
- ✅ **Remote access** via 0.0.0.0:4838

## Installation

### Prerequisites

- Python 3.10 or higher
- Ollama installed and running
- At least one Ollama model (e.g., `ollama pull llama2`)

### Installation

1. **Clone repository or extract files**

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Adjust configuration** (optional):
```bash
cp env.example .env
# Edit .env if needed
```

## Usage

### Start Server

```bash
# Direct
python -m mcp_server.server

# Or with start script
./start.sh

# Or with uvicorn
uvicorn mcp_server.server:app --host 0.0.0.0 --port 4838
```

The server runs by default on **0.0.0.0:4838**.

### API Endpoints

#### Health Check
```bash
curl http://localhost:4838/health
```

#### List Tools
```bash
curl -X POST http://localhost:4838/mcp/tools/list
```

#### Call Tool
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_list_models",
    "arguments": {}
  }'
```

#### JSON-RPC 2.0
```bash
curl -X POST http://localhost:4838/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## Available Tools

### Model Management
- `ollama_list_models` - Lists all models
- `ollama_show_model` - Shows model details
- `ollama_pull_model` - Downloads model
- `ollama_delete_model` - Deletes model
- `ollama_copy_model` - Copies model
- `ollama_create_model` - Creates model from modelfile

### Text Generation
- `ollama_generate` - Generates text
- `ollama_generate_stream` - Streaming generation

### Chat Functions
- `ollama_chat` - Chat completion
- `ollama_chat_stream` - Streaming chat

### Embeddings
- `ollama_embeddings` - Generate embeddings
- `ollama_create_embeddings` - Batch embeddings

### System & Monitoring
- `ollama_check_health` - Health check
- `ollama_get_version` - Ollama version
- `ollama_list_processes` - Running processes
- `ollama_get_models_info` - All model info

### Additional Tools
- `ollama_update_model` - Update model
- `ollama_get_modelfile` - Get modelfile
- `ollama_validate_model` - Validate model
- `ollama_get_model_size` - Model size
- `ollama_search_models` - Search models
- `ollama_check_blobs` - Blob status
- `ollama_save_context` - Save context
- `ollama_load_context` - Load context
- `ollama_clear_context` - Clear context
- `ollama_batch_generate` - Batch generation
- `ollama_compare_models` - Compare models

## Configuration

### Environment Variables

Create a `.env` file:

```env
# MCP Server Configuration
MCP_HOST=0.0.0.0
MCP_PORT=4838

# Ollama API Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Firewall Configuration

For remote access, port 4838 must be opened:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 4838/tcp

# firewalld (RHEL/CentOS)
sudo firewall-cmd --add-port=4838/tcp --permanent
sudo firewall-cmd --reload
```

## Example Usage

### Python Client

```python
import httpx

# Call tool
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:4838/mcp/tools/call",
        json={
            "name": "ollama_generate",
            "arguments": {
                "model": "llama2",
                "prompt": "Explain Python in one sentence.",
            }
        }
    )
    print(response.json())
```

### cURL Examples

#### Generate Text
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_generate",
    "arguments": {
      "model": "llama2",
      "prompt": "What is Machine Learning?"
    }
  }'
```

#### Chat
```bash
curl -X POST http://localhost:4838/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ollama_chat",
    "arguments": {
      "model": "llama2",
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }
  }'
```

## Project Structure

```
RL-MCP Server/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py          # Main server
│       ├── client.py          # Ollama API client
│       ├── config.py          # Configuration
│       ├── handlers.py        # Tool handlers
│       ├── exceptions.py      # Exceptions
│       └── utils/             # Utilities
├── tests/                      # Tests
├── examples/                   # Examples
├── requirements.txt           # Dependencies
├── pyproject.toml            # Project configuration
├── README_DE.md              # German version
├── README_EN.md              # This file
└── LICENSE                   # License
```

## Development

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## License

See [LICENSE](LICENSE) file.

## Author

**Robin Oliver Lucas**
- Website: https://rl-dev.de
- Email: robin@rl-dev.de

## Support

For questions or issues, please create an issue or contact the author.

## Additional Information

- [Installation Guide](INSTALL.md)
- [Plan & Architecture](PLAN.md)
- [Checklist](CHECKLIST.md)

