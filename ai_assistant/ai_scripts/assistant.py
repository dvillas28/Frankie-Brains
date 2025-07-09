from abc import ABC, abstractmethod
import os
import base64

class Assistant(ABC):
    
    def __init__(self, name: str, api_key: str) -> None:
        self.name: str = name
        self.api_key = api_key
        self.prompt = """" 
    
    Actúa como docente de Lengua y Literatura para 7° y 8° básico. Debes entregar una retroalimentación para el texto del estudiante que aparece en la imagen. Tu retroalimentación debe centrarse específicamente en el Objetivo de Aprendizaje 19: ""Escribir textos organizados en párrafos diferenciados temáticamente, precisos y cohesionados, mediante el correcto uso de la puntuación, diversos mecanismos de mantención del referente y una variedad de marcadores y conectores". 

    Incluye estos 4 elementos en tu retroalimentación: 
        - "👍 Lo que has logrado"": Un comentario positivo sobre algo que el estudiante logró correctamente según el Objetivo de Aprendizaje 19.
        - "📝 Para mejorar la organización"": Una observación sobre cómo mejorar la organización de la información (marcadores discursivos y conectores), con un ejemplo concreto extraído del texto.
        - "❓ Para reflexionar"": Una pregunta que guíe al estudiante a mejorar la progresión temática o profundidad temática de su texto.
        - "✨ Mejorando correferencias"": Un ejemplo específico que muestre cómo mejorar la mantención del referente (sustituyendo palabras repetidas por pronombres, sinónimos, hipónimos, hiperónimos o anáforas).

    Límite: 150 palabras máximo 
    Tono: Positivo y adecuado para un estudiante de 13-14 años 
    Formato: Usa subtítulos e íconos para facilitar la lectura"
    Formato de salida: Debes entregar 1 linea en el siguiente formato:
        👍 Lo que has logrado;[contenido]
        📝 Para mejorar la organizacion;[contenido]
        ❓ Para reflexionar;[contenido]
        ✨ Lo que has logrado;[contenido]
    Entrega solamente esa linea, nada mas, nada menos.
    """
    
    # Function to encode the image
    def encode_image(self, image_path: str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process_image(self, image_path: str) -> dict:

        if os.path.exists(image_path):
            try:
                base64_image = self.encode_image(image_path)                
                response = self.make_request(self.prompt, base64_image)
                
                # response = '👍 Lo que has logrado;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n📝 Para mejorar la organización;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n❓ Para reflexionar;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n✨ Mejorando correferencias;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

                # self.save_result(image_path, response)
                response_list = self.format_response(response)
    
                return {
                    "valid": True,
                    "result": response_list
                }
                                

            except Exception as e:
                print(f"Error al procesar la imagen {image_path}: {e}")
                return {
                    "valid": False,
                    "result": "Ha ocurrido un error en la API al procesar la imagen"
                }

        else:
            print(f"La imagen {image_path} no existe")
            return {
                "valid": False,
                "result": "La imagen tomada no se guardo correctamente"
            }
    
    @abstractmethod
    def make_request(self, prompt: str, base64_image):
        pass
     
    def save_result(self, image_path: str, response: str) -> None:
        image_name = os.path.splitext(os.path.basename(image_path))[0]

        results_base_folder = os.path.join("ai_assistant", "ai_results")
        image_results_folder = f"results_{image_name}"

        results_folder = os.path.join(results_base_folder, image_results_folder)

        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        result_file_path = os.path.join(results_folder, f"{image_name}_response_{self.name}.txt")

        with open(result_file_path, 'w', encoding='utf-8') as file:
            file.write(response)

        print(f"Response guardado en: {result_file_path}")

    def format_response(self, response: str) -> list[list[str]]:
        lista = response.strip().split("\n")

        for i in range(len(lista)):
            lista[i] = lista[i].strip().split(";")

        return lista