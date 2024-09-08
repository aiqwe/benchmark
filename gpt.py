import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
default_role = {
    "translator": "I want you to ac as an English translator and NLP engineer. \
     Translate the text that I give you from English to Korean. \
     Respond in Markdown"
}


def chat(text: str, model="gpt-4o-2024-08-06", role: str = "translator"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": default_role[role]},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return completion.choices[0].message.content
