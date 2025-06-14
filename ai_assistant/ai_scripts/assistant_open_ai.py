import os
from assistant import Assistant
from openai import OpenAI

class Gpt(Assistant):
    
    def __init__(self, name: str, api_key: str):
        super().__init__(name, api_key)
        self.client = OpenAI(api_key=self.api_key)

    def process_image(self, image_path: str) -> None:

        if os.path.exists(image_path):
            try:
                base64_image = self.encode_image(image_path)
                response = self.make_request(self.prompt, base64_image)
                
                # response = 'test'

                print(response)
                self.save_result(image_path, response)

            except Exception as e:
                print(f"Error al procesar la imagen {image_path}: {e}")

        else:
            print(f"La imagen {image_path} no existe")

    def make_request(self, prompt: str, base64_image):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": f"{prompt}" },
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