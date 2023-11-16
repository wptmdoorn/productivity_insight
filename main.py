import time
from jinja2 import Environment, FileSystemLoader
import openai
import os
import pdfkit
from llm import get_screenshot_keywords, get_summary

# load OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

INTERVAL_SECONDS = 10

starttime = time.monotonic()
summaries = {}

info = {
    'start_time': time.strftime("%Y-%m-%d %H:%M:%S"),
    'interval': os.environ["INTERVAL_KEYWORD_SEC"],
    'summary': '',
    'tips': '',
    'keywords': ''
}


def generate_html(info: dict):
    template = Environment(loader=FileSystemLoader(
        'templates')).get_template('report_template.html')

    return template.render(info=info)


info = {
    'start_time': time.strftime("%Y-%m-%d %H:%M:%S"),
    'interval': os.environ["INTERVAL_KEYWORD_SEC"],
    'summary': '',
    'tips': '',
    'keywords': ''
}

summaries = {}

while True:
    summaries[f'{time.strftime("%Y-%m-%d %H:%M:%S")}'] = get_screenshot_keywords()
    print(summaries)

    if len(summaries) >= int(os.environ["OBSERVATIONS_PER_DOCUMENT"]):
        s = get_summary(summaries)
        print(s)

        info['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        info['keywords'] = " <br/> ".join(
            [f'{key} - {value}' for key, value in summaries.items()])
        info['summary'] = s['summary']
        info['tips'] = s['tips']

        file_name = f"Summary and Productivity ({time.strftime('%Y_%m_%d_%H_%M')}).pdf"

        pdfkit.from_string(generate_html(
            info), os.path.join('output', file_name))

        summaries = {}

        info = {
            'start_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'interval': int(os.environ["INTERVAL_KEYWORD_SEC"]),
            'summary': '',
            'tips': '',
            'keywords': ''
        }

    time.sleep(int(os.environ["INTERVAL_KEYWORD_SEC"]) -
               ((time.monotonic() - starttime) % int(os.environ["INTERVAL_KEYWORD_SEC"])))
