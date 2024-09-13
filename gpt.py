import os
from openai import OpenAI

DEFAULT_ROLE = {
    "translator": "I want you to ac as an English translator and NLP engineer. \
     Translate the text that I give you from English to Korean. \
     Respond in Markdown. \
     output format should be splitted by new line and mark '\n' delimeter each end of line."
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
            {"role": "assistant", "content": role},
            {"role": "user", "content": text},
        ]
    )

    return completion.choices[0].message.content
