from dotenv import load_dotenv
import os
import requests

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print

# =========================
# 🌦️ Weather Tool
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"Weather in {city}: {desc}, {temp}°C"


# =========================
# 📰 News Tool (Tavily)
# =========================

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )
    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"
    news_list = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")
        news_list.append(f"- {title}\n  🔗 {url}\n  📝 {snippet[:100]}...")
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# =========================
# 🧠 LLM + Tools Setup
# =========================

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm = ChatMistralAI(model="mistral-small-latest")
llm_with_tools = llm.bind_tools([get_weather, get_news])


# =========================
# ✅ Human in the Loop
# =========================

def human_approval(tool_call) -> bool:
    """Ask for human approval before every tool call."""
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    confirm = input(f"\n🔔 Agent wants to call '[bold yellow]{tool_name}[/bold yellow]' with {tool_args}\n   Approve? (yes/no): ")
    return confirm.lower() == "yes"


# =========================
# 🤖 Agent Loop
# =========================

print("\n[bold cyan]🏙️  City Agent[/bold cyan] | Type [bold red]exit[/bold red] to quit\n")

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("[bold red]Goodbye! 👋[/bold red]")
        break

    messages.append(HumanMessage(user_input))
    result = llm_with_tools.invoke(messages)
    messages.append(result)

    # Tool calls handle karo
    while result.tool_calls:
        for tool_call in result.tool_calls:
            tool_name = tool_call["name"]

            # Human approval
            if human_approval(tool_call):
                tool_message = tools[tool_name].invoke(tool_call)
                print(f"[dim]✅ Tool '{tool_name}' executed[/dim]")
            else:
                tool_message = ToolMessage(
                    content="Tool call denied by user.",
                    tool_call_id=tool_call["id"]
                )
                print(f"[dim]❌ Tool '{tool_name}' denied[/dim]")

            messages.append(tool_message)

        result = llm_with_tools.invoke(messages)
        messages.append(result)

    print(f"\n[bold green]Bot:[/bold green] {result.content}\n")