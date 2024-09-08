# This is the initial version of the code
# The code requires some beautification and cleanup
import ast
import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI()


class SummaryContent(BaseModel):
    summary: str


class WebURL(BaseModel):
    url: str


class WebURLs(BaseModel):
    urls: List[WebURL]


class BrowseWeb:
    system_prompt: str = """
    you are an expert in crafting a correct https web link based on user input.
    """

    user_prompt: str = """
    please create the https web link based on the below input \n
    {input}
    """

    summary_system_prompt = """
    You are a helpful summarizing agent. Please provide a detailed summary of the 
    provided content. Ensure that the summary is comprehensive and easy to understand.
    The summary must cover all important points in the content and must be at least 1500 words.
    """

    def summarize_content(self, text):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content":self.summary_system_prompt},
                {
                    "role": "user",
                    "content": "Please summarize the below content \n content:\n{text}".format(text=text)
                }
            ],
            response_format=SummaryContent,
        )

        return ast.literal_eval(json.loads(json.dumps(completion.choices[0].message.content)))["summary"]


    def generate_web_link(self, input):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": self.user_prompt.format(input=input)
                }
            ],
            response_format=WebURL,
        )

        url = ast.literal_eval(json.loads(json.dumps(completion.choices[0].message.content)))

        return url["url"]

    def get_link_text(self, image_url):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract only the hyperlink of the arxiv papers in the image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_url}",
                            },
                        },
                    ],
                }
            ],
            response_format=WebURLs,
            max_tokens=300,
        )
        urls = ast.literal_eval(json.loads(json.dumps(completion.choices[0].message.content)))['urls']
        return urls

    def summarize_content_of_a_link(self, image_url, existing_summary):
        prompt = """
        You will be provided an existing summary.
        Create a new summary with the content of the existing summary and the content of the image.
        existing summary:
        {existing_summary}
        """.format(existing_summary=existing_summary)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_url}",
                            },
                        },
                    ],
                }
            ],
            response_format=SummaryContent,
            max_tokens=300,
        )

        return completion.choices[0].message.content
