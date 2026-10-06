import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_weather(city: str) -> str:
    """Gets the current weather for a city.

    Args:
        city: The name of the city.

    Returns:
        A simple weather result.
    """

    print(f"\nTOOL CALLED: get_weather({city})")

    return f"The weather in {city} is 27 degrees Celsius."


response = client.models.generate_content(
    model="gemini-3.8-flash",

    contents="What is the weather in Bangalore?",

    config={
        "tools": [get_weather]
    }
)

print("\nGEMINI:")
print(response.text)