import pygame as pg
from pygame import Surface
import cv2

from config import args, COLOR_BACKGROUND, COLOR_CONFIRM, COLOR_REJECT, FPS
from camera import find_camera, initialize_camera, set_rotation_angle, take_photo
from screen import draw_text, draw_wrapped_text, flash_screen, initialize_font
from events import handle_events

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

    # Accion a tomar luego de un evento
    action: str = ''

    while running:
        # search for camera()
        if not camera_found:
            camera_index = find_camera()
            if camera_index is not None:
                
                cap = initialize_camera(camera_index)
                camera_found = True

        screen.fill(COLOR_BACKGROUND)

        # video()
        if camera_found and cap is not None:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.transpose(frame) # corregir rotacion si es que
                frame_surface = pg.surfarray.make_surface(frame)

                # Ajustar tamaño para que la imagen ocupe todo el ancho de la pantalla
                win_w, win_h = screen.get_size()

                if args["show"]:
                    # Escalar la imagen para que ocupe todo el ancho de la pantalla
                    bar_size = 250
                    target_w = win_w - (2 * bar_size)
                    target_h = win_h

                    # Escalar la imagen sin mantener la proporción
                    frame_surface = pg.transform.scale(frame_surface, (target_w, target_h))

                    # Aplicar rotación
                    frame_surface = pg.transform.rotate(frame_surface, rotation_angle)

                    # Calcular la posición para centrar la imagen
                    if rotation_angle in [90, 270]:
                        x_offset = (win_w - target_h) // 2
                        y_offset = (win_h - target_w) // 2
                    else:
                        x_offset = (win_w - target_w) // 2
                        y_offset = (win_h - target_h) // 2

                    # Dibujar la imagen en la pantalla
                    screen.blit(frame_surface, (x_offset, y_offset))

                # Mostrar texto independiente de si estamos mostrando la camara
                draw_text(screen, f"Orientación: {args['orientation'].upper()}", 0, 0)

                # Mostrar la rotacion actual en base a la orientacion predeterminada
                draw_text(screen, f"Rotación actual: {rotation_angle}°", 0, 20)
                
                # Controles
                draw_text(screen, "<p>: tomar una foto", 0, win_h // 2)
                draw_text(screen, "<q>: cerrar programa", 0, win_h // 2 + 20)
                draw_text(screen, "<s>: mostrar camara", 0, win_h // 2 + 20*2)
                draw_text(screen, "<Esc>: fullscreen", 0, win_h // 2 + 20*3)
                draw_text(screen, "<Arrow Keys>: rotar", 0, win_h // 2 + 20*4)

            if photo_taken:
                draw_wrapped_text(screen, f"Foto guardada en: {filepath}", win_w - 500, win_h // 2, 250)            
                draw_text(screen, f"Borrosa?: {is_blurry}", 0, win_h // 2 + 20*5)     

        else:
            draw_text(screen, "Buscando cámara...", screen_width // 2 - 150, screen_height // 2)
        
        # Manejo de eventos
        running, action = handle_events(custom_events)
        match action:
            case '':
                # no hacer nada
                pass

            case 'try_to_take_photo':
                if camera_found:

                    filepath, is_blurry = take_photo(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if is_blurry:
                        flash_screen(screen, color=COLOR_REJECT)

                    else:
                        flash_screen(screen, color=COLOR_CONFIRM)

                    photo_taken = True
                    pg.time.set_timer(photo_taken_Event, 5000)

            case 'photo_taken':
                pg.time.set_timer(photo_taken_Event, 0)
                photo_taken = False

            case 'toggle_fullscreen':
                screen, fullscreen = toggle_fullscreen(fullscreen, screen_width, screen_height)

            case 'toggle_camera':
                toggle_camera()

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