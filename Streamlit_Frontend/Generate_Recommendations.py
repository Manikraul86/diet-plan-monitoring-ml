import requests
import json

class Generator:
    def __init__(self, nutrition_input: list, ingredients: list = None, params: dict = None):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients if ingredients is not None else []
        self.params = params if params is not None else {'n_neighbors': 5, 'return_distance': False}

    def set_request(self, nutrition_input: list, ingredients: list, params: dict):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params

    def generate(self):
        payload = {
            'nutrition_input': self.nutrition_input,
            'ingredients': self.ingredients,
            'params': self.params
        }

        try:
            response = requests.post(
                url='http://127.0.0.1:8080/predict/',
                json=payload,  # ✅ use json= instead of data=
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            # ✅ Debugging info
            print("Status code:", response.status_code)
            print("Response text:", response.text[:500])  # Print first 500 chars for safety

            response.raise_for_status()  # Raises HTTPError for 4xx/5xx

            return response  # Caller can still use .json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
