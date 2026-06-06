from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


model = ChatMistralAI(model="mistral-small-2506")
parser = StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generator"),
    ("human", "{topic}")
])

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains code in simple terms"),
    ("human", "Explain the following code in simple words:\n{code}")
])

sequence = code_prompt | model | parser 


sequence2 = RunnableParallel(
    {"code" :  RunnablePassthrough(),
     "explanation" : explain_prompt | model | parser
    }
)

chain = sequence | sequence2 

result = chain.invoke({"topic" : "please write a code of palindrome in java "})

print(result['code'])
print(result['explanation'])

# Notes :-
#> First, the user topic goes into code_prompt. The code_prompt creates a proper prompt using the topic and sends it to the model. The model generates a code response, but the response is in LangChain's message format. Then StrOutputParser extracts only the text part from that response and returns it as a normal string. This generated code becomes the output of sequence.

#> Now the output of sequence (the generated code) is passed to sequence2. Inside sequence2, there are two parallel branches because RunnableParallel runs multiple tasks at the same time.

#> In the first branch, the code goes to RunnablePassthrough(). RunnablePassthrough does not modify anything. Whatever input it receives, it returns the exact same output. So the generated code is returned as it is and stored in the "code" key.

#> In the second branch, the same generated code goes into explain_prompt. The {code} placeholder inside the prompt is replaced with the generated code. This new prompt is sent to the model, which reads the code and generates an explanation. Then StrOutputParser extracts the explanation text from the model's response and returns it as a normal string. This explanation is stored in the "explanation" key.

#> Finally, RunnableParallel combines the outputs of both branches and returns a dictionary containing the original generated code and its explanation.



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Flow of data:-
# Topic
#   ↓
# code_prompt
#   ↓
# model
#   ↓
# StrOutputParser
#   ↓
# Generated Code (sequence output)
#   ↓
# RunnableParallel
#   ├── RunnablePassthrough → Same Code → "code"
#   │
#   └── explain_prompt
#           ↓
#         model
#           ↓
#     StrOutputParser
#           ↓
#       Explanation → "explanation"

# Final Output:
# {
#    "code": generated_code,
#    "explanation": explanation
# }