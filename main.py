from utils.assistant_gemini import Gemini
from utils.assistant_gpt import Gpt
from utils.events import handle_events
from utils.screen import (
    initialize_font,
    draw_text,
    draw_debug_menu,
    flash_screen,
    pygame_blit_surface,
    scale_backgrounds,
    blit_background_to_screen,
    draw_result)
from utils.camera import find_camera, initialize_camera, set_rotation_angle, take_photo
from utils.internet import connected_to_internet
from utils.config import (
    args,
    COLOR_GREEN,
    FPS)
import os
from threading import Thread
from dotenv import load_dotenv
import pygame as pg
from pygame import Surface
import cv2

load_dotenv()

# Crear al asistente de IA

match args["assistant"]:
    case "gemini":
        if not os.getenv("GEMINI_API_KEY"):
            print("Error: GEMINI_API_KEY not found on env")
            exit(-1)

        assistant = Gemini(api_key=os.getenv("GEMINI_API_KEY"))

    case "gpt":
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not found on env")
            exit(-1)

        assistant = Gpt(api_key=os.getenv("OPENAI_API_KEY"))

    case _:
        print(f"Assistant {args['assistant']} not valid")
        exit(-1)


def toggle_fullscreen(fullscreen: bool, screen_width: int, screen_height: int) -> Surface | bool:
    fullscreen = not fullscreen
    if fullscreen:
        pg.mouse.set_visible(False)
        return pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN), fullscreen
    else:
        pg.mouse.set_visible(True)
        return pg.display.set_mode((800, 600)), fullscreen


def toggle_camera() -> None:
    args["show"] = not args["show"]


def toggle_debug_menu() -> None:
    args["debug"] = not args["debug"]


def main() -> None:
    pg.init()
    initialize_font()

    # Variables pantalla
    info = pg.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen: Surface = pg.display.set_mode(
        (screen_width, screen_height), pg.FULLSCREEN | pg.SCALED)
    fullscreen: bool = True

    # Transformar el tamaño de los fondos y ocultar el cursor
    scale_backgrounds(screen_width, screen_height)
    pg.mouse.set_visible(False)

    # Variables para el loop principal
    clock = pg.time.Clock()
    running: bool = True
    camera_found: bool = False
    cap = None  # objeto de la camara
    internet_connection: bool = False

    # Eventos
    custom_events = dict()
    photo_taken: bool = False
    photo_taken_Event = pg.USEREVENT + 1
    custom_events["photo_taken_Event"] = photo_taken_Event

    # Accion a tomar luego de un evento
    action: str = ''

    # Variables para la camara
    rotation_angle: int = set_rotation_angle()

    # Variables para la imagen tomada
    filepath: str = ''        # path del archivo a guardar
    done_processing: bool = True  # API procesando imagen
    result = None  # resultados del llamado a la API

    def process_image_thread(filepath: str, prompt_type: str) -> None:
        nonlocal result, done_processing
        done_processing = False
        result = assistant.process_image(filepath, prompt_type)
        done_processing = True

    while running:
        # Mantenerse buscando una camara la cual conectarse
        if not camera_found:
            camera_index = find_camera()
            if camera_index is not None:

                cap = initialize_camera(camera_index)
                camera_found = True

        # Mantenerse revisando si se esta conectado a internet
        if not internet_connection:
            internet_connection = connected_to_internet()

        # Mostrar imagen de fondo dependiendo del estado de la cámara
        blit_background_to_screen(screen, cam_found=camera_found,
                                  inet_connection=internet_connection)

        # video()
        if camera_found and cap is not None and internet_connection:
            ret, frame = cap.read()
            if ret:

                # Transdormar el frame a una superficie de pygame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.transpose(frame)  # corregir rotacion si es que

                frame_surface = pg.surfarray.make_surface(frame)

                # Ajustar tamaño para que la imagen ocupe todo el ancho de la pantalla
                win_w, win_h = screen.get_size()

                if args["show"]:
                    pygame_blit_surface(
                        screen, frame_surface, win_w, win_h, rotation_angle)

                # Menu debug
                draw_debug_menu(screen, win_w, win_h, rotation_angle)

            if photo_taken:
                # Acciones cuando una foto fue tomada. Nada por ahora
                pass

            # Mostrar si se esta procesando un llamado
            if not done_processing:
                draw_text(True, screen, "Cargando...",
                          win_w // 2 - 50, win_h // 2)

            # Mostrar si el resultado ya fue procesado y esta listo
            if done_processing and result:
                draw_result(screen=screen,
                            dims=(screen_width, screen_height),
                            data=result)

        # No hay camara o no hay conexión a internet
        else:
            if not (camera_found and cap is not None):
                draw_text(False, screen, "Buscando cámara...",
                          screen_width // 2 - 150, screen_height // 2)

            elif not internet_connection:
                draw_text(False, screen, "No hay conexión a Internet",
                          screen_width // 2 - 150, screen_height // 2)

        # Manejo de eventos
        running, action = handle_events(
            custom_events=custom_events,
            result_is_none=(lambda: True if result else False)()
        )

        match action:
            case '':
                # no hacer nada
                pass

            # Este patron comprueba si la accion es del tipo 'try_to_take_photo:?' (? es una wildcard)
            case action if action.startswith('try_to_take_photo:'):
                if camera_found:

                    filepath = take_photo(
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

                    # Obtener el tipo de prompt a utilizar con el asistente
                    prompt_type: str = (lambda: action.split(':')[1])()

                    th = Thread(target=process_image_thread,
                                args=(filepath, prompt_type,))
                    th.start()

                    flash_screen(screen, color=COLOR_GREEN)
                    photo_taken = True
                    pg.time.set_timer(photo_taken_Event, 5000)

            case 'clear_result':
                result = None
                photo_taken = False
                blit_background_to_screen(
                    screen, cam_found=camera_found, inet_connection=internet_connection)

            case 'photo_taken':
                pg.time.set_timer(photo_taken_Event, 0)
                photo_taken = False

            case 'toggle_fullscreen':
                screen, fullscreen = toggle_fullscreen(
                    fullscreen, screen_width, screen_height)

            case 'toggle_camera':
                toggle_camera()

            case 'toggle_debug_menu':
                toggle_debug_menu()

            case 'rotate_left':
                # 90° a la izquierda
                rotation_angle = (rotation_angle - 90) % 360

            case 'rotate_right':
                # 90° a la derecha
                rotation_angle = (rotation_angle + 90) % 360

        pg.display.flip()
        clock.tick(FPS)

    if cap:
        cap.release()
    pg.quit()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
