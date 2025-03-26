import json
import env
from mistralai import Mistral

def get_prompt():
    prompt_file = open("./prompt.md", encoding = "utf8")
    prompt = prompt_file.read()
    prompt_file.close()
    return prompt

MODEL = env.get("MISTRAL_MODEL")
API_KEY = env.get("MISTRAL_API_KEY")

prompt = get_prompt()

client = Mistral(
    api_key = API_KEY
)

def get_key_queries(name, description):
    response = client.chat.complete(
        model = MODEL,
        messages = [
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": "Понял, давай начнем. Отправьте, пожалуйста, входные данные в указанном формате."
            },
            {
                "role": "user",
                "content": f"Название: {name}. Описание {description}"
            }
        ]
    )

    key_queries = json.loads(response.choices[0].message.content)
    
    return key_queries
