import os
from assistant_open_ai import Gpt
from assistant_gemini import Gemini
from dotenv import load_dotenv

load_dotenv()

gpt = Gpt(
    name='openai',
    api_key=os.getenv("OPENAI_API_KEY")
)

gemini = Gemini(
    name='gemini',
    api_key=os.getenv("GEMINI_API_KEY")
)

if __name__=="__main__":
    BASE_PATH = os.path.join("motion_blur", "dataset_Respuestas_estudiantes_PRAC", "orig")
    image_path = os.path.join(BASE_PATH, "IMG_0017.jpg")
    
    # gpt.process_image(image_path)
    gemini.process_image(image_path)
