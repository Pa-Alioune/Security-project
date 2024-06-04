# app/utils/token_utils.py
import json


def store_token(token):
    with open("token.json", "w") as token_file:
        json.dump({"token": token}, token_file)


def get_token():
    try:
        with open("token.json", "r") as token_file:
            data = json.load(token_file)
            return data.get("token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None
