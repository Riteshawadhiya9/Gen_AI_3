from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearchResults(max_result = 5)

llm = ChatMistralAI(model = "mistral-small-2506")

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant

summarize the following news into clear bullet points

{news}
"""
)

chain = prompt | llm | StrOutputParser()

news_result = search_tool.run("latest news on AI of 2026")

result = chain.invoke({"news" : news_result})
print("------------------------------------------------------------------------------------------------")

print(result)

print("------------------------------------------------------------------------------------------------")

print("------------------------------------------------------------------------------------------------")
print(f"Description: {search_tool.description}")
print("------------------------------------------------------------------------------------------------")
print(f"Name: {search_tool.name}")
print("------------------------------------------------------------------------------------------------")
print(f"Arguments: {search_tool.args}")