import ast
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI()

class SummaryContent(BaseModel):
    article_id:int
    article_name:str
    summary: str

class ImageRead():

    def read_and_sumamrize_image_content(self, image_url,existing_summary):
        prompt = """
        You will be provided an existing summary.
        Create a new summary with the content of the existing summary and the content of the image.
        Please ensure to provide a detailed and comprehensive summary of only the content under 
        Article <article_id>:<topic>. DO NOT miss any key content while summarizing. 
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
            response_format=SummaryContent
        )

        return ast.literal_eval(json.loads(json.dumps(completion.choices[0].message.content)))["summary"]
