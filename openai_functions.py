import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def get_chat_completion(system_message="You are a summariser. Summarise only the text in the user input. Do not add any new information. Do not include your opinion.", user_message="This is a test"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="gpt-4-0125-preview",
    )
    return chat_completion.choices[0].message.content
