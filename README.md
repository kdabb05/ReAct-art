# ReAct-art: CLI ReAct Agent for Art, Books, Coffee, and Matcha

A simple, from-scratch CLI ReAct agent that answers questions and uses tools for art, books, coffee, and matcha. No agentic libraries used—just standard Python and `requests`.

## Features
- ReAct (Reasoning + Acting) loop with tool use
- Tools for art search, book recommendation, coffee and matcha facts
- Uses OpenRouter API for LLM completions
- CLI interface: one question per run

## Setup
1. **Python 3.8+ required**
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Place your OpenRouter API key in a file named `.openrouter_api_key` in the project root (this file is gitignored):
   ```
   sk-...your_openrouter_key...
   ```

## Usage
```bash
python main.py "Recommend a book about art"
```


## File Structure
- `main.py` — CLI entry point
- `react_agent.py` — ReAct agent logic
- `llm.py` — OpenRouter API integration
- `tools.py` — Tool functions (see below)

## Tool Overview

| Tool Name               | Purpose                                      | Uses HTTP? | Returns JSON? | Notes                                  |
|------------------------|----------------------------------------------|:----------:|:-------------:|-----------------------------------------|
| get_artworks_by_artist | Returns artworks by artist (hardcoded data)  |     No     |     Yes       | Local data only                         |
| search_books_by_title  | Searches books by title (hardcoded data)     |     No     |     Yes       | Local data only                         |
| coffee_shop_near       | Finds nearby coffee shop via Geoapify API    |    Yes     |     Yes       | Requires `GEOAPIFY_API_KEY` env var     |
| matcha_trend_data      | Gets weather & matcha trend via Open-Meteo   |    Yes     |     Yes       | No API key needed (Open-Meteo is free)  |

**Notes:**
- Both `coffee_shop_near` and `matcha_trend_data` make HTTP requests to remote web services and return JSON structured data.
- The other tools use only local, hardcoded data and also return JSON.

## Notes
- Each CLI call is stateless (no memory between runs)
- The `.openrouter_api_key` file must exist in the project root
- No agentic libraries (LangChain, CrewAI, etc.) are used
- For `coffee_shop_near`, set the `GEOAPIFY_API_KEY` environment variable with your Geoapify API key.