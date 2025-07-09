import os
from threading import Thread
from dotenv import load_dotenv
import pygame as pg
from pygame import Surface
import cv2

load_dotenv()

from utils.config import args, COLOR_CONFIRM, COLOR_REJECT, FPS, CAMERA_NOT_FOUND_PATH, CAMERA_FOUND_PATH
from utils.internet import connected_to_internet
from utils.camera import find_camera, initialize_camera, set_rotation_angle, take_photo
from utils.screen import (initialize_font,
                    draw_text,
                    draw_list_items,
                    draw_debug_menu,
                    flash_screen,
                    pygame_blit_surface,)
from utils.events import handle_events
from ai_assistant.ai_scripts.assistant_gemini import Gemini


assistant = Gemini(
    name='assistant',
    api_key=os.getenv("GEMINI_API_KEY")
)

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
    screen: Surface = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN | pg.SCALED)
    pg.mouse.set_visible(False)

    clock = pg.time.Clock()
    fullscreen: bool = True

    # Carga de imagenes de fondo
    camera_not_found_image = pg.image.load(CAMERA_NOT_FOUND_PATH)
    camera_not_found_image = pg.transform.scale(camera_not_found_image, (screen_width, screen_height))
    
    camera_found_image = pg.image.load(CAMERA_FOUND_PATH)
    camera_found_image = pg.transform.scale(camera_found_image, (screen_width, screen_height))

    # TODO: Imagen de no conexión a internet

    # Variables para el loop principal
    running: bool = True
    camera_found: bool = False
    cap = None # objeto de la camara
    internet_connection: bool = False

    # Eventos
    custom_events = dict()
    photo_taken: bool = False
    photo_taken_Event = pg.USEREVENT + 1
    custom_events["photo_taken_Event"] = photo_taken_Event

    # Variables para la camara
    rotation_angle: int = set_rotation_angle()

    # Variables para la imagen tomada
    filepath: str = ''
    is_blurry: bool = ''

    processing: bool = False
    result: dict = dict()

    def process_image_thread(filepath: str) -> None:
        nonlocal result, processing
        processing = True
        result = assistant.process_image(filepath)
        processing = False

    # Accion a tomar luego de un evento
    action: str = ''

    while running:
        # search for camera()
        if not camera_found:
            camera_index = find_camera()
            if camera_index is not None:
                
                cap = initialize_camera(camera_index)
                camera_found = True

        if not internet_connection:
            internet_connection = connected_to_internet()

        # Mostrar imagen de fondo dependiendo del estado de la cámara
        # TODO: Mostrar imagen cuando no haya conexión a internet
        if camera_found and internet_connection:
            screen.blit(camera_found_image, (0, 0))
        else:
            screen.blit(camera_not_found_image, (0, 0))

        # video()
        if camera_found and cap is not None and internet_connection:
            ret, frame = cap.read()
            if ret:
                
                # Transdormar el frame a una superficie de pygame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.transpose(frame) # corregir rotacion si es que
                
                frame_surface = pg.surfarray.make_surface(frame)

                # Ajustar tamaño para que la imagen ocupe todo el ancho de la pantalla
                win_w, win_h = screen.get_size()

                if args["show"]:
                    pygame_blit_surface(screen, frame_surface, win_w, win_h, rotation_angle)

                # Menu debug
                draw_debug_menu(screen, win_w, win_h, rotation_angle)

            if photo_taken:
                # draw_wrapped_text(True, screen, f"Foto guardada en: {filepath}",
                #                   win_w - 500, win_h // 2, 250)            
                draw_text(False, screen, f"Borrosa?: {is_blurry}", 0, win_h // 2 + 20*5)

            # Mostrar si se esta procesando un llamado
            if processing:
                draw_text(True, screen, "Cargando...", win_w // 2 - 50, win_h // 2)     

            # Mostrar si el resultado ya fue procesado y esta listo
            if not processing and result:
                
                # Dibujar un cuadrado donde irán los resultados 
                rect_width, rect_height = screen_width - 200, screen_height - 200
                rect_x, rect_y = 100, 100
                rect_color = (128, 128, 128)

                pg.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

                # Rectangulo para el texto
                rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)

                
                if result["valid"]:
                    draw_list_items(screen, result['result'], rect, font_size=30, title_color=(255, 255, 255), message_color=(200, 200, 200))
                
                else:
                    draw_list_items(screen,  [["Error", "Hubo un error con la API"]], rect, font_size=24, title_color=(255, 255, 255), message_color=(200, 200, 200))
        else:
            if not(camera_found and cap is not None):
                draw_text(True, screen, "Buscando cámara...", screen_width // 2 - 150, screen_height // 2)

            elif not internet_connection:
                draw_text(True, screen, "No hay conexión a Internet", screen_width // 2 - 150, screen_height // 2)
        
        # Manejo de eventos
        running, action = handle_events(custom_events, result)
        match action:
            case '':
                # no hacer nada
                pass

            case 'try_to_take_photo':
                if camera_found:

                    filepath, is_blurry = take_photo(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    
                    if not is_blurry:
                        th = Thread(target=process_image_thread, args=(filepath,))
                        th.start()

                    flash_screen(screen, color=COLOR_CONFIRM if is_blurry else COLOR_REJECT)
                    photo_taken = True
                    pg.time.set_timer(photo_taken_Event, 5000)

            case 'clear_result':
                result = dict()
                photo_taken = False
            
            case 'photo_taken':
                pg.time.set_timer(photo_taken_Event, 0)
                photo_taken = False

            case 'toggle_fullscreen':
                screen, fullscreen = toggle_fullscreen(fullscreen, screen_width, screen_height)

            case 'toggle_camera':
                toggle_camera()

            case 'toggle_debug_menu':
                toggle_debug_menu()

            case 'rotate_left':
                rotation_angle = (rotation_angle - 90) % 360 # 90° a la izquierda

            case 'rotate_right':
                rotation_angle = (rotation_angle + 90) % 360 # 90° a la derecha

                
        pg.display.flip()
        clock.tick(FPS)


    if cap:
        cap.release()
    pg.quit()


if __name__ == '__main__':
    main()