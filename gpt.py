import os
from openai import OpenAI

DEFAULT_ROLE = {
    "translator": "I want you to act as an English translator and NLP engineer also. \
     Translate the text that I give you from English to Korean. \
     You should keep lexical nuance and vocabularies when translating from English to. \
     Output format should be follwed below: \
     - Respond in Markdown. \
     - output format should be splitted by new line each sentence."
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
            {"role": "user", "content": "{role}\n---\n{text}".format(role=role, text=text)},
        ]
    )

    return completion.choices[0].message.content
