from utils.assistant import Assistant
from openai import OpenAI


class Gpt(Assistant):

    def __init__(self, api_key: str):
        super().__init__('GPT', api_key)
        self.client = OpenAI(api_key=self.api_key)

    def make_request(self, prompt: str, base64_image):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        )

        return completion.choices[0].message.content
