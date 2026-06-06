from langchain.tools import tool


@tool #decorator for creating tool 
def get_greeting(name : str) -> str: #type hints
    """Generate a greeting message for a user""" #docstring

    return f"Hello {name}, Welcome to the AI world"


result = get_greeting.invoke({"name":"Ritesh"})
print("------------------------------------------------------------------------------------------------")
print(result)
print("------------------------------------------------------------------------------------------------")

print("------------------------------------------------------------------------------------------------")
print(f"Tool Name: {get_greeting.name}")
print("------------------------------------------------------------------------------------------------")
print(f"Description: {get_greeting.description}")
print("------------------------------------------------------------------------------------------------")
print(f"Arguments: {get_greeting.args}")