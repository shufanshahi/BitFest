import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

INGREDIENTS_API_URL = "http://127.0.0.1:8000/api/ingredients/"
CUISINES_API_URL = "http://127.0.0.1:8000/api/cuisines/create"

model = OllamaLLM(model="llama2")


PROMPT_TEMPLATE = """
Your job is to suggest recipes based on available ingredients and user's requirements.
User's requirement: {query}
Available Ingredients: {ingredients}
Strictly follow the below JSON format to suggest a recipe:
{{
    "name": "",
    "taste": "",
    "review": "",
    "type": "",
    "prep_time": 
}}
"""

def fetch_ingredients():
    try:
        response = requests.get(INGREDIENTS_API_URL)
        response.raise_for_status()  
    
        ingredients = response.json()
        available_ingredients = ""
        
    
        for ingredient in ingredients:
            available_ingredients += f"ID: {ingredient['id']}, Name: {ingredient['name']}, Amount: {ingredient['amount']}\n"
        
        return available_ingredients  
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch ingredients: {e}")
        return None


def generate_and_post_cuisine(query):
    try:
        available_ingredients = fetch_ingredients()

        formatted_prompt = PROMPT_TEMPLATE.format(query=query, ingredients=available_ingredients)


        prompt = ChatPromptTemplate.from_template(formatted_prompt)
        

        llm_response = model.generate_prompt(prompt)

        response_str = llm_response.generations[0].text.strip()
        
        cuisine_data = json.loads(response_str) 

        post_response = post_cuisine(CUISINES_API_URL, cuisine_data)
        

        return post_response
    except Exception as e:
        raise Exception(f"Error in generating and posting cuisine: {e}")


def post_cuisine(api_url, cuisine_data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=cuisine_data, headers=headers)
        if response.status_code == 201:  
            return response.json()
        else:
            raise Exception(f"Failed to post cuisine. Status code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        raise Exception(f"Error posting cuisine: {e}")

if __name__ == "__main__":
    user_query = input("Enter your requirement for a recipe: ")
    try:
        result = generate_and_post_cuisine(user_query)
        print("Cuisine successfully created:", result)
    except Exception as e:
        print(str(e))