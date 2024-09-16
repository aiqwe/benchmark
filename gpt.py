import os
from openai import OpenAI

DEFAULT_ROLE = {
    "translator": """
    Translate below <|text|> to Korean and you should keep below format:
      - You should say naturally.
      - I want you to act as a NLP expert.
      - You should keep lexical nuance using NLP words.
      - You should keep your tone like saying to layman.
    <|text|>
    """
}


def chat(
    text: str,
    model="o1-preview-2024-09-12",
    role: str = DEFAULT_ROLE["translator"],
    api_key: str = None,
):
    if not api_key:
        api_key = os.environ["OPENAI_API_KEY"]

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "{role}{text}".format(role=role, text=text)},
        ],
    )

    return completion.choices[0].message.content
