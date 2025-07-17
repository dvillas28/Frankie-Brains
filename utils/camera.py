# camera.py
"""
Funciones que tienen que ver con la camara y la toma de fotos
"""

import os
import cv2
from cv2 import VideoCapture
from datetime import datetime

# from utils.detect_blur import check_blur
from utils.config import args


def find_camera(start_range: int = 0) -> int | None:
    # Buscar una cámara conectada
    """
    Obtener el indice de la camara, encuentra la primera disponible.
    """

    # TODO: hallar una manera mas elegente de hacer esto
    if os.name == 'nt':
        start_range = 1  # hack para saltarse la camara de defecto

    ranges = (start_range,10)
    for i in range(*ranges):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None


def initialize_camera(index: int) -> VideoCapture:
    """
    Inicializar la camara en base al indice encontrado.
    Tambien setea la calidad de la camara
    """

    cap = cv2.VideoCapture(index)

    quality = int(args["quality"])

    if quality:

        # Resolucion de alta calidad
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    else:

        # Resolucion de baja calidad
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    return cap


def set_rotation_angle() -> int:
    """
    Calcular el parametro de rotacion en funcion de la orientacion actual de la camara.
    """

    rot = 0
    orientation = args["orientation"].lower()

    match orientation:
        case "n":
            rot = (rot) % 360

        case "o":
            rot = (rot + 90) % 360

        case "s":
            rot = (rot + 180) % 360

        case "e":
            rot = (rot - 90) % 360

    return rot


def rotate_frame(frame):
    """
    Rotar el frame en base a la orientacion recibida en los argumentos.
    """
    orientation = args["orientation"].lower()

    match orientation:

        case "n":
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # La orientacion Oeste no necesita rotacion
        # case "O":

        case "s":
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        case "e":
            frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Revertir la imagen
    return cv2.flip(frame, 0)


def take_photo(frame) -> str:
    """
    Procesar el frame de esa iteración.
    Guardarlo como una imagen .jpg.
    """

    o = args["orientation"].upper()
    
    if not os.path.exists(os.path.join("/", "home", os.environ["USER"], "pyCamera")):
        abspath = os.path.join("/", "home", os.environ["USER"], "Frankie-Brains")
    else:
        abspath = os.path.join("/", "home", os.environ["USER"], "pyCamera")
    
    pics_dir = os.path.join(abspath, "output", "camera_pics")
    os.makedirs(pics_dir, exist_ok=True)

    frame = rotate_frame(frame)

    now = datetime.now()
    filename = now.strftime("%Y_%m_%d-%H-%M-%S") + f"_{o}" + ".jpg"
    filepath = os.path.join(pics_dir, filename)

    cv2.imwrite(filepath, frame)
    print(f"Foto guardada en: {filepath}")

    return filepath
