from abc import ABC, abstractmethod
import os
import base64
from utils.config import args, DEMO_MODE_OUTPUT
from utils.prompts import prompts
from utils.result import Result


class Assistant(ABC):
    """
    Clase abstracta de un asistente de IA
    """

    def __init__(self, name: str, api_key: str) -> None:
        self.name: str = name
        self.api_key = api_key
        self.prompts: dict = prompts

    # Function to encode the image
    def encode_image(self, image_path: str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process_image(self, image_path: str, prompt_type: str) -> Result:

        if os.path.exists(image_path):
            try:

                if args["demo"]:
                    response_list = self.format_response(DEMO_MODE_OUTPUT)

                else:

                    # Realizar el llamado y guardar el resultado
                    base64_image = self.encode_image(image_path)
                    response = self.make_request(
                        self.prompts[prompt_type], base64_image)
                    self.save_result(image_path, response)

                    # TODO 1: El formato del prompt depende del tipo
                    response_list = self.format_response(response)

                return Result(
                    valid=True,
                    data=response_list,
                    result_type=prompt_type
                )

            except Exception as e:
                print(f"Error al procesar la imagen {image_path}: {e}")

                return Result(
                    valid=False,
                    data="Ha ocurrido un error en la API al procesar la imagen"
                )

        else:
            print(f"La imagen {image_path} no existe")
            return Result(
                valid=False,
                data="La imagen tomada no se guardo correctamente"

            )

    @abstractmethod
    def make_request(self, prompt: str, base64_image):
        pass

    def save_result(self, image_path: str, response: str) -> None:
        image_name = os.path.splitext(os.path.basename(image_path))[0]

        if not os.path.exists(os.path.join("/", "home", os.environ["USER"], "pyCamera")):
            abspath = os.path.join("/", "home", os.environ["USER"], "Frankie-Brains")
        else:
            abspath = os.path.join("/", "home", os.environ["USER"], "pyCamera")
        
        results_base_folder = os.path.join(abspath, "output", "ai_results")
        image_results_folder = f"results_{image_name}"

        results_folder = os.path.join(
            results_base_folder, image_results_folder)

        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        result_file_path = os.path.join(
            results_folder, f"{image_name}_response_{self.name}.txt")

        with open(result_file_path, 'w', encoding='utf-8') as file:
            file.write(response)

        print(f"Response guardado en: {result_file_path}")

    def format_response(self, response: str) -> list[list[str]]:
        lista = response.strip().split("\n")

        for i in range(len(lista)):
            lista[i] = lista[i].strip().split(";")

        return lista
