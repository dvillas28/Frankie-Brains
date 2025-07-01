from ai_assistant.ai_scripts.assistant import Assistant
# from assistant import Assistant
from google import genai
from google.genai import types

class Gemini(Assistant):

    def __init__(self, name: str, api_key: str):
        super().__init__(name, api_key)
        self.client = genai.Client(api_key=self.api_key)

    def make_request(self, prompt, base64_image):
        
        image_part = types.Part.from_bytes(
            data=base64_image,
            mime_type='image/jpeg',
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image_part, prompt]
        )

        return response.text