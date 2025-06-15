import os
from threading import Thread
from dotenv import load_dotenv
import pygame as pg
from pygame import Surface
import cv2

from utils.config import args, COLOR_CONFIRM, COLOR_REJECT, FPS, CAMERA_NOT_FOUND_PATH, CAMERA_FOUND_PATH
from utils.camera import find_camera, initialize_camera, set_rotation_angle, take_photo
from utils.screen import (initialize_font,
                    draw_text,
                    draw_wrapped_text,
                    draw_debug_menu,
                    flash_screen,
                    pygame_blit_surface,)
from utils.events import handle_events
from ai_assistant.ai_scripts.assistant_gemini import Gemini

load_dotenv()

gemini = Gemini(
    name='gemini',
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

    # Variables para el loop principal
    running: bool = True
    camera_found: bool = False
    cap = None # objeto de la camara

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
    result_gemini: dict = dict()

    def process_image_thread(filepath: str) -> None:
        nonlocal result_gemini, processing
        processing = True
        result_gemini = gemini.process_image(filepath)
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

        # screen.fill(COLOR_BACKGROUND)

        # Mostrar imagen de fondo dependiendo del estado de la cámara
        if camera_found:
            screen.blit(camera_found_image, (0, 0))
        else:
            screen.blit(camera_not_found_image, (0, 0))

        # video()
        if camera_found and cap is not None:
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

            if processing:
                draw_text(True, screen, "Cargando...", win_w // 2 - 50, win_h // 2)     

            if not processing and result_gemini:
                if result_gemini["valid"]:
                    for i, item in enumerate(result_gemini["result"]):
                        title, message = item
                        draw_text(True, screen, title, 10, 10 + i * 60)  # Parte superior izquierda
                        draw_wrapped_text(True, screen, message, 10, 30 + i * 60, 400)  # Ajustar debajo del título
                else:
                    draw_text(True, screen, result_gemini["result"], win_w // 2 - 50, win_h // 2)     
        else:
            draw_text(False, screen, "Buscando cámara...",
                      screen_width // 2 - 150, screen_height // 2)
        
        # Manejo de eventos
        running, action = handle_events(custom_events)
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