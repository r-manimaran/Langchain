# Simple LangChain Agent

A beginner-friendly project demonstrating how to build AI agents using [LangChain](https://www.langchain.com/) with Google Gemini as the LLM backend.

## Project Structure

```
1. SimpleAgent/
├── main.py          # Basic agent - asks Gemini a question and prints the response
├── Toolcall.py      # Agent with tools - weather and time tools using faker for mock data
├── .env             # API keys (not committed)
├── .env.example     # Example env file
└── requirements.txt # Dependencies
```

## Features

- **main.py** — Creates a simple LangChain agent and queries Gemini for topics on Agentic AI
- **Toolcall.py** — Creates an agent with two tools:
  - `get_weather(location)` — Returns randomized fake weather data (condition, temperature, humidity)
  - `get_current_utc_time()` — Returns the current UTC time

## Prerequisites

- Python 3.10+
- A [Google AI API key](https://aistudio.google.com/app/apikey)

## Setup

1. Clone the repo and navigate to this folder:
   ```shell
   cd "1. SimpleAgent"
   ```

2. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your API key:
   ```shell
   cp .env.example .env
   ```
   ```
   GOOGLE_API_KEY=<your_google_api_key>
   ```

## Usage

Run the basic agent:
```shell
python main.py
```

Run the agent with tools:
```shell
python Toolcall.py
```

## Dependencies

- `langchain` — Agent orchestration framework
- `langchain-google-genai` — Google Gemini LLM integration
- `faker` — Generates random fake data for mock tools
- `python-dotenv` — Loads environment variables from `.env`
