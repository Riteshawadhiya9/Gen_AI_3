# Gen AI Projects Suite 🚀

A comprehensive collection of AI-powered applications demonstrating advanced LangChain patterns, LLM orchestration, and intelligent tool usage. This suite includes multiple projects showcasing production-ready implementations.

## 📋 Table of Contents

- [Projects Overview](#projects-overview)
  - [PulseAI](#pulseai--live-news-intelligence)
  - [City Agent](#city-agent--intelligent-city-information)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Component Documentation](#component-documentation)
- [Contributing](#contributing)

## 🎯 Projects Overview

### PulseAI — Live News Intelligence
An intelligent news summarization platform that:
- Fetches real-time news using Tavily Search API
- Processes news articles with multiple LLM providers
- Implements various LangChain runnable patterns
- Provides a modern, interactive Streamlit UI
- Demonstrates production-ready LLM chain patterns

**Key Files:** `UI_News_Summarizer.py`, `newssummarizer.py`

### City Agent — Intelligent City Information
An advanced AI-powered agent system that:
- Provides real-time weather information for any city
- Retrieves the latest news about specific cities
- Demonstrates sophisticated tool-calling patterns
- Implements multi-turn agent conversations
- Showcases LLM tool binding and execution
- Features safety approval mechanisms for tool usage

**Key Files:** `UI_City_Agent.py`, `Agents.py`, `toolcalling.py`

## ✨ Features

### PulseAI Features
- Real-time news fetching via Tavily Search API
- Multi-LLM support (Mistral, OpenAI, Google GenAI, Groq)
- Sequential and parallel chain patterns
- Modern dark-themed Streamlit UI
- Customizable summarization prompts

### City Agent Features
- Real-time weather data integration (OpenWeather API)
- Dynamic news retrieval for cities
- Sophisticated tool-calling and binding
- Multi-turn agent conversations
- Tool approval interface for safety
- Beautiful gradient UI with message history

### Shared Capabilities
- Advanced chain patterns (sequential, parallel, passthrough)
- Vector search with FAISS and ChromaDB
- Document processing (PDF parsing, web scraping)
- Environment-based API key management
- Production-ready error handling

## 📁 Project Structure

```
Gen_AI_3/
├── UI_News_Summarizer.py           # Main Streamlit UI for news summarization
├── UI_City_Agent.py                # Streamlit UI for intelligent city agent
├── Agents.py                       # Agent implementations with weather & news tools
├── newssummarizer.py               # Core news summarization logic
├── owntool.py                      # Custom tool implementations
├── toolcalling.py                  # Tool calling patterns with LLMs
├── parallelrunnables.py            # Parallel chain execution patterns
├── sequencerunnable.py             # Sequential chain patterns
├── runnablepassthrough.py          # Passthrough runnable patterns
├── test.py                         # Test suite
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys)
└── README.md                       # This file
```

## 🛠 Technology Stack

### Core LLM Frameworks
- **LangChain**: Main framework for LLM orchestration
- **LanGraph**: Graph-based workflow orchestration
- **LangChain Community**: Extended LLM integrations

### LLM Providers
- Mistral AI
- OpenAI
- Google GenAI
- Groq

### Data Processing
- FAISS (CPU) - Vector similarity search
- ChromaDB - Vector database
- BeautifulSoup4 - Web scraping
- PyPDF - PDF document parsing
- TikToken - Token counting

### Web Framework
- Streamlit - Interactive UI framework
- FastAPI - Optional API backend
- Uvicorn - ASGI server

### Utilities
- python-dotenv - Environment variable management
- requests - HTTP client
- lxml - XML/HTML processing

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip or UV package manager
- API keys for LLM providers (Mistral, OpenAI, Google GenAI, Groq, Tavily)

### Installation Steps

1. **Clone/Navigate to the project directory**:
   ```bash
   cd Gen_AI_3
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or using UV:
   ```bash
   uv pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with your API keys:

```env
# LLM Provider Keys
OPENAI_API_KEY=your_openai_key
MISTRAL_API_KEY=your_mistral_key
GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key

# Search & Weather API
TAVILY_API_KEY=your_tavily_key
OPENWEATHER_API_KEY=your_openweather_key

# Optional: Other configurations
LANGCHAIN_DEBUG=false
```

The application uses `python-dotenv` to automatically load these variables.

## 📖 Usage

### 🔥 PulseAI — News Summarizer

#### Run the UI
```bash
streamlit run UI_News_Summarizer.py
```

**Features:**
- Search for news on any topic
- Get AI-powered summaries with bullet points
- Customize summarization prompts
- Dark-themed modern interface
- Real-time news processing

**Access:** `http://localhost:8501`

---

### 🏙️ City Agent — City Information System

#### Run the UI
```bash
streamlit run UI_City_Agent.py
```

**Features:**
- Ask questions about cities naturally
- Get real-time weather information
- Receive latest city news automatically
- Interactive multi-turn conversations
- Tool approval interface for safety
- Beautiful gradient UI with chat history
- Seamless tool integration

**Access:** `http://localhost:8501`

---

### Running Individual Components

#### Tool Calling
```bash
python toolcalling.py
```
Interactive console demonstrating tool binding and LLM tool invocation.

#### Agents
```bash
python Agents.py
```
Demonstrates agent implementations with weather and news tools.

#### News Summarizer
```bash
python newssummarizer.py
```
Demonstrates basic news fetching and summarization.

#### Parallel Runnables
```bash
python parallelrunnables.py
```
Shows how to execute multiple chains in parallel for different outputs on the same or different topics.

#### Sequential Runnables
```bash
python sequencerunnable.py
```
Demonstrates chain composition and sequential execution patterns.

#### Runnable Passthrough
```bash
python runnablepassthrough.py
```
Shows passthrough patterns for data flow management.

### Running Tests

```bash
python test.py
```

## 📚 Component Documentation

### PulseAI Components

#### UI_News_Summarizer.py
The main Streamlit application for news summarization:
- Custom CSS styling with dark theme
- Interactive search interface
- Real-time news processing
- Response streaming
- Error handling and user feedback

**Key Functions:**
- Page configuration and styling
- News search input handling
- LLM chain execution
- Results display and formatting

#### newssummarizer.py
Core summarization logic demonstrating:
- Integration with Tavily Search API
- LLM chain construction
- Output parsing
- Tool inspection

**Usage Example:**
```python
from newssummarizer import search_tool, chain

news = search_tool.run("latest AI news")
summary = chain.invoke({"news": news})
```

---

### City Agent Components

#### UI_City_Agent.py
An intelligent city agent Streamlit application featuring:
- Interactive chat interface with gradient styling
- Multi-turn conversations with full history
- Tool calling with approval mechanism
- Real-time weather and news retrieval
- Beautiful gradient UI with message bubbles
- Tool use transparency and control

**Key Features:**
- Weather queries for any city
- Latest news retrieval for cities
- Tool approval interface for safety
- Message history and streaming responses
- Responsive design with custom CSS

#### Agents.py
Core agent implementations providing:
- **get_weather()** tool - Fetches current weather using OpenWeather API
- **get_news()** tool - Retrieves latest news using Tavily Search
- Tool decorators for LLM integration
- Rich formatting for output display

**Example Tools:**
```python
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    # Returns temperature and weather description

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    # Returns latest news articles
```

#### toolcalling.py
Demonstrates LLM tool calling patterns:
- Tool creation and binding
- LLM-tool integration
- Interactive conversation loop
- Tool invocation and response handling

**Pattern Example:**
```python
llm_with_tool = llm.bind_tools([tool1, tool2, ...])
message = HumanMessage(user_input)
result = llm_with_tool.invoke(message)
if result.tool_calls:
    # Execute tool and continue conversation
```

---

### Shared Components (Used by Both Projects)

### Shared Components (Used by Both Projects)

#### parallelrunnables.py
Advanced pattern showing:
- `RunnableParallel` for concurrent execution
- `RunnableLambda` for custom transformations
- Multiple chain branches
- Different prompts on same/different data

#### sequencerunnable.py
Basic chain pattern demonstrating:
- `ChatPromptTemplate` construction
- Model selection
- `StrOutputParser` for output formatting
- Simple pipe operator chain composition

#### runnablepassthrough.py
Pattern showing:
- Data passthrough mechanisms
- Intermediate data retention
- Complex chain routing

#### owntool.py
Custom tool implementations for:
- Domain-specific operations
- Utility functions
- Extended functionality

#### test.py
Test suite for validating:
- Chain outputs
- Tool functionality
- Integration scenarios

## 🔧 Extending the Projects

### Extending PulseAI

#### Add a News Source
1. Create a new search tool or integrate a different news API
2. Modify the summarization chain to handle the new format
3. Update the UI to allow source selection

#### Customize Summarization
1. Modify the prompt in `newssummarizer.py`
2. Add custom output parsing logic
3. Implement topic-specific summarization strategies

### Extending City Agent

#### Creating Tool-Calling Agents
Define tools using the `@tool` decorator and bind them to an LLM:

```python
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

@tool
def my_tool(input_str: str) -> str:
    """Tool description"""
    return result

llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tools = llm.bind_tools([my_tool])

message = HumanMessage("Ask the AI something")
result = llm_with_tools.invoke([message])

if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_output = my_tool.invoke(result.tool_calls[0])
```

#### Adding a New Tool to City Agent
1. Define a new tool function in `Agents.py`:
   ```python
   @tool
   def get_population(city: str) -> str:
       """Get population of a city"""
       # Your implementation
       return population_info
   ```

2. Update the agent to use the new tool by binding it to the LLM

#### Add More City Data
1. Integrate additional APIs (population, landmarks, events, etc.)
2. Create new tools for each data source
3. Update the agent's tool list

### Shared Extensions

#### Adding a New LLM Provider
1. Add the provider SDK to `requirements.txt`
2. Configure API key in `.env`
3. Import and initialize in your chain:
   ```python
   from langchain_provider import ChatProvider
   model = ChatProvider(model="model-name")
   ```

#### Creating Custom Chains
1. Create a new Python file for your chain logic
2. Use `ChatPromptTemplate`, model, and parser
3. Compose using the pipe operator (`|`)
4. Test with the provided test suite

#### Building Custom Tools
Extend `owntool.py` with:
```python
from langchain_community.tools import Tool

def custom_function(input_str):
    # Your logic
    return result

custom_tool = Tool(
    name="tool_name",
    func=custom_function,
    description="Tool description"
)
```

## 📊 Architecture Patterns Used

1. **LangChain LCEL** (LangChain Expression Language)
   - Pipe operator chaining
   - Declarative chain composition

2. **Runnable Abstractions**
   - Sequential execution
   - Parallel processing
   - Custom transformations

3. **Tool Integration & Tool Calling**
   - Tool binding to LLMs
   - Automatic tool invocation
   - Tool use transparency
   - Safety approval mechanisms

4. **Agent Patterns**
   - Tool-augmented LLMs
   - Multi-turn conversations
   - Stateful message management
   - Tool result integration

5. **Tool Integration**
   - External API integration (Tavily, OpenWeather)
   - Custom tool wrappers
   - Tool decorators

6. **Vector Search**
   - FAISS for similarity search
   - ChromaDB for persistent storage

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch
2. Implement changes with clear commit messages
3. Test thoroughly
4. Submit a pull request with documentation

## 📝 License

This project is provided as-is for educational and development purposes.

## 🆘 Troubleshooting

### General Issues

**Issue: "API key not found"**
- Solution: Ensure `.env` file exists in project root with correct API keys

**Issue: Streamlit port already in use**
- Solution: Run on different port: `streamlit run <app>.py --server.port 8502`

**Issue: Import errors**
- Solution: Ensure virtual environment is activated and dependencies installed: `pip install -r requirements.txt`

**Issue: Slow responses**
- Solution: Use faster models or reduce `max_results` in search tool

### PulseAI Issues

**Issue: News not fetching**
- Solution: Verify `TAVILY_API_KEY` is valid and quota hasn't been exceeded

**Issue: Slow summarization**
- Solution: Use `mistral-small-2506` model instead of larger models for faster responses

### City Agent Issues

**Issue: Tools not being called**
- Solution: Ensure the LLM is properly bound with tools using `llm.bind_tools([tools])`

**Issue: Weather data not fetching**
- Solution: Verify `OPENWEATHER_API_KEY` is valid and city name is spelled correctly

**Issue: News not showing up**
- Solution: Check `TAVILY_API_KEY` is valid and your Tavily quota hasn't been exceeded

**Issue: Tool approval interface not showing**
- Solution: Ensure Streamlit session state is properly initialized

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review component documentation
3. Examine example scripts for usage patterns
4. Verify API keys and environment configuration

---

**Built with ❤️ using LangChain, LanGraph, and Python**
