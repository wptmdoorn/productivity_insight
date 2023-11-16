import json
import openai
import os
from io import BytesIO
from pyautogui import screenshot
import base64

# load OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_screenshot_keywords():
    output = BytesIO()
    screenshot().save(output, format='JPEG')

    image_data = base64.b64encode(output.getvalue()).decode()

    try:
        s = openai.OpenAI().chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze the screenshot of my desktop. Summarize the contents of the screenshot in max 10 words."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ],
                }
            ],
            max_tokens=300,
        )

        print(s)

        return s.choices[0].message.content
    except Exception as e:
        print(e)
        return "No information was retrieved from the screenshot."


def get_summary(dict_of_keywords: dict) -> str:
    observations = " \n".join(
        [f'{key} - {value}' for key, value in dict_of_keywords.items()])

    prompt = f"""
        I will show you a list timestamps with keywords wthat were observed from screenshots of my desktop.
        Can you first please shortly summarize what I've been doing on my computer? Next, can you give
        me some concrete advice on how to improve my productivity? Please list at least three points.

        The observations are:
        {observations}
    """

    try:
        return json.loads(openai.OpenAI().chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                    "content": "You are designed to output a JSON object with the keys 'summary' and 'tips'. Each key should have only one value with a multi-line string."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": prompt},

                    ],
                }
            ],
            max_tokens=600,
        ).choices[0].message.content)
    except:
        return "No summary could be given."
