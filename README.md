# LangChain Agent with FastAPI

A simple backend implementation of a LangChain agent using FastAPI and uv for dependency management.

## Overview

This project demonstrates how to create a web API that exposes a LangChain agent's capabilities. The agent uses the ReAct framework to process user queries and leverages tools like web search to provide informative responses.

## Features

- FastAPI backend with RESTful endpoint
- LangChain ReAct agent implementation
- Environment management with uv
- Web search capability through Tavily

## Setup

### Prerequisites

- Python 3.8+
- uv package manager

### Installation

1. Clone this repository.
2. Run the setup script:

```bash
# Windows
setup.bat

# Alternative manual setup
uv init
uv venv
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS
uv pip install -r requirements.txt
```

3.Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY="your_openai_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

## Usage

### Start the server

```bash
uv run fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- **POST /chat**
  - Request body: `{"message": "Your query here"}`
  - Returns: `{"response": "Agent's response"}`

### Example

Using curl:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Rio de Janeiro?"}'
```

## API Documentation

When the server is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
