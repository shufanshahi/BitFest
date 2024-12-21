import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

# API URLs
INGREDIENTS_API_URL = "http://127.0.0.1:8000/api/ingredients/"
CUISINES_API_URL = "http://127.0.0.1:8000/api/cuisines/create"

# Define the model
model = OllamaLLM(model="llama2")

# Define the prompt structure
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

# Fetch available ingredients from the API
def fetch_ingredients(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            ingredients_data = response.json()  # Assuming the API returns a JSON object with a list of ingredients
            # Assuming each ingredient is a dictionary with a 'name' key (adjust if necessary)
            ingredients = [ingredient['name'] for ingredient in ingredients_data]  # Extract ingredient names
            return ingredients
        else:
            raise Exception(f"Failed to fetch ingredients. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching ingredients: {e}")

# Generate and post a recipe
# Generate and post a recipe
def generate_and_post_cuisine(query):
    try:
        # Step 1: Fetch ingredients
        available_ingredients = fetch_ingredients(INGREDIENTS_API_URL)
        ingredients = ", ".join(available_ingredients)  # Convert list to a string for the prompt

        # Step 2: Create prompt
        formatted_prompt = PROMPT_TEMPLATE.format(query=query, ingredients=ingredients)

        # Step 3: Use LangChain to generate cuisine data
        prompt = ChatPromptTemplate.from_template(formatted_prompt)
        output_parser = JsonOutputParser()

        # Adjusting to ensure that the response is properly parsed
        llm_response = model.generate_prompt(prompt, output_parser=output_parser)

        # Assuming llm_response is a tuple, extract the response from it
        response_str = llm_response[0]  # This should be the string part of the response

        # Parse the LLM's response to JSON
        cuisine_data = json.loads(response_str)

        # Step 4: Post generated cuisine
        post_response = post_cuisine(CUISINES_API_URL, cuisine_data)

        # Step 5: Return the final response
        return post_response
    except Exception as e:
        raise Exception(f"Error in generating and posting cuisine: {e}")


# Post cuisine data to the API
def post_cuisine(api_url, cuisine_data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=cuisine_data, headers=headers)
        if response.status_code == 201:  # Assuming 201 for successful creation
            return response.json()
        else:
            raise Exception(f"Failed to post cuisine. Status code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        raise Exception(f"Error posting cuisine: {e}")

# Example usage
if __name__ == "__main__":
    # Take user query as input
    user_query = input("Enter your requirement for a recipe: ")
    try:
        result = generate_and_post_cuisine(user_query)
        print("Cuisine successfully created:", result)
    except Exception as e:
        print(str(e))