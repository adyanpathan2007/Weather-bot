import os

from dotenv import load_dotenv
from google import genai

from weather import get_weather


# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Load our skill
with open("weather_skill.md", "r", encoding="utf-8") as file:
    weather_skill = file.read()


# Create a conversation
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "system_instruction": weather_skill,
        "tools": [get_weather],
    }
)


print("Weather Agent started!")
print("Type 'exit' to quit.")


while True:

    user_message = input("\nYou: ")

    if user_message.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        response = chat.send_message(user_message)

        print("\nAgent:")
        print(response.text)

    except Exception as e:
        print("\nSomething went wrong:")
        print(e)