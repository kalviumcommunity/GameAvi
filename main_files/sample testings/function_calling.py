import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

functions = {
    "get_build_guide": {
        "description": "Get the best build guide for a specific game",
        "parameters": {
            "type": "object",
            "properties": {
                "game": {"type": "string"},
                "level": {"type": "string"}
            },
            "required": ["game", "level"]
        }
    },
    "get_quest_tips": {
        "description": "Get quest tips for a specific game and quest name",
        "parameters": {
            "type": "object",
            "properties": {
                "game": {"type": "string"},
                "quest_name": {"type": "string"}
            },
            "required": ["game", "quest_name"]
        }
    }
}

def get_build_guide(game, level):
    return f"For {game}, best build at {level} is focusing on Strength and Vigor."

def get_quest_tips(game, quest_name):
    return f"Tips for {quest_name} in {game}: Explore hidden paths and talk to NPCs twice."
user_query = input("Ask GameAvi anything (e.g., Best build in Elden Ring?): ")

response = model.generate_content(
    user_query,
    tools=[{"function_declarations": [functions["get_build_guide"], functions["get_quest_tips"]]}]
)

if response.candidates[0].content.parts[0].function_call:
    func_call = response.candidates[0].content.parts[0].function_call
    func_name = func_call.name
    args = func_call.args

        print(f"AI wants to call function: {func_name} with arguments {args}")

        if func_name == "get_build_guide":
        print(get_build_guide(args["game"], args["level"]))
    elif func_name == "get_quest_tips":
        print(get_quest_tips(args["game"], args["quest_name"]))
else:
    print(response.text)