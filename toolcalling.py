from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool 
from langchain_core.messages import HumanMessage
from rich import print 

#1 creating a tool 
@tool
def get_text_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)

tools = {
    "get_text_length" : get_text_length
}
llm = ChatMistralAI(model = "mistral-small-2506")

#tool binding 
llm_with_tool = llm.bind_tools([get_text_length])

message = []

print("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("[bold green]AI:[/bold green] Hello! I am an AI assistant. I can help you with various tasks. Just ask me anything!")
print("If you want to \"quit\" chat just write \"exit\".. \n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------\n")

while True:
    prompt = input("You: ")
    
    if prompt.lower() == "exit":
        break
    
    query = HumanMessage(prompt)
    message.append(query)

    result = llm_with_tool.invoke(message)
    message.append(result)

    if result.tool_calls:
        tool_name = result.tool_calls[0]["name"]
        tool_message = tools[tool_name].invoke(result.tool_calls[0])
        message.append(tool_message)
        result = llm_with_tool.invoke(message)
    
    print(f"[bold green]AI:[/bold green] {result.content}")

# Tool kab chalega?
# Jab tu text length ke baare mein poochhe — tabhi get_text_length tool call hoga!
# You: What is the length of text "Python"?
# ✅ Tool chalega → 6 return karega
# You: What is AI?
# ❌ Tool nahi chalega → directly answer dega