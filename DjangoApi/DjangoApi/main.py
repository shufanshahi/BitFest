from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

model = OllamaLLM(model="llama2")

str_output_parser = StrOutputParser()
json_output_parser = JsonOutputParser()

prompt=""" 
your only job is to suggest recipes based on available ingredients and user's requirement
User's requirement: {query}\n
Available Ingredients:{ingredients}\n
strictly follow the below format to suggest recipes
{{
    "name": "",
    "taste": "",
    "review": "",
    "type": "",
    "prep_time": 
}}
  
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        # MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}"),
    ]
)


recipeBot = qa_prompt | model | str_output_parser


# recipeBot.invoke({"query": "human"})