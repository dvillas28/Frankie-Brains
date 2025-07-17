# screen.py
"""
Funciones que actuan sobre la pantalla
"""

import pygame as pg
from pygame import Surface
from utils.config import (args, BAR_SIZE, COLOR_BLACK, COLOR_WHITE,
                          DEBUG_FONT, RESULTS_FONT,
                          NOTFOUND_NOINTERNET,
                          NOTFOUND_INTERNET,
                          FOUND_NOINTERNET,
                          FOUND_INTERNET,
                          BACKGROUND,
                          )
from utils.result import Result

font = None

# Carga de imagenes de fondo
notfound_nointernet = pg.image.load(NOTFOUND_NOINTERNET)
notfound_internet = pg.image.load(NOTFOUND_INTERNET)
found_nointernet = pg.image.load(FOUND_NOINTERNET)
found_internet = pg.image.load(FOUND_INTERNET)
background = pg.image.load(BACKGROUND)


def initialize_font():
    """
    La font debe ser inicializada despues de ejecutar pg.init().
    """
    global font
    font = pg.font.SysFont(DEBUG_FONT, 18)


def draw_text(always: bool, screen: Surface, text: str, x: int, y: int, color: tuple = COLOR_BLACK) -> None:
    """
    Dibuja texto en la pantalla en la posicion (x, y).
    """

    #  Si queremos mostrar el debug o si queremos mostrar el mensaje independiente de si estamos en debug o no
    if args["debug"] or always:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    return


def draw_centered_text(screen: Surface, text: str, rect: pg.Rect, font_size: int, color: tuple) -> None:
    """
    Dibuja texto centrado dentro de un rectángulo en la pantalla.
    """
    font = pg.font.SysFont(DEBUG_FONT, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_result(screen: Surface, dims: tuple, data: Result) -> None:
    """
    Dibuja los resultados a la pantalla. El tipo de dibujo depende del resultado del prompt 
    (tipo de prompts, o si este falló)
    """

    # Aplicar el fondo donde irá el rectangulo de resultados
    blit_background_to_screen(screen=screen, show_result=True)

    # Dibujar un rectangulo donde irán los resultados
    rect_width, rect_height = dims[0] - 200, dims[1] - 200
    rect_x, rect_y = 100, 50
    pg.draw.rect(screen, COLOR_WHITE,
                 (rect_x, rect_y, rect_width, rect_height))

    # Rectangulo para el texto
    rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)

    if data.valid:
        if data.result_type == "REVISION":
            draw_list_items(
                screen=screen,
                items=data.data,
                rect=rect,
                font_size=35,
                title_color=COLOR_BLACK,
                message_color=COLOR_BLACK
            )

        elif data.result_type == "PLANIFICACION":
            # TODO 2: Aun no tenemos definido el formato de salida de este prompt
            # A lo mejor habria que definir un prompt generico de dibujo
            draw_centered_text(
                screen=screen,
                text='PLANIFICACION',
                rect=rect,
                font_size=24,
                color=COLOR_BLACK
            )

    else:
        draw_centered_text(
            screen=screen,
            text=data.data,
            rect=rect,
            font_size=24,
            color=COLOR_BLACK
        )


def draw_list_items(screen: Surface, items: list, rect: pg.Rect, font_size: int, title_color: tuple, message_color: tuple) -> None:
    """
    Dibuja una lista de listas de la forma [título y mensaje)] dentro de un rectángulo en la pantalla.
    """
    font_title = pg.font.SysFont(RESULTS_FONT, font_size)
    # Mensaje con fuente más pequeña
    font_message = pg.font.SysFont(RESULTS_FONT, font_size - 4)

    # Margen interno dentro del rectángulo
    padding = 20
    x, y = rect.x + padding, rect.y + padding

    max_width = rect.width - (2 * padding)  # ancho máximo

    for title, message in items:
        # Renderizar el título
        title_surface = font_title.render(title, True, title_color)
        screen.blit(title_surface, (x, y))
        y += font_title.get_height() + 10  # Espacio entre título y mensaje

        # Dividir el mensaje en líneas si excede los 150 caracteres
        words = message.split(' ')
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font_message.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # Renderizar la línea actual y comenzar una nueva
                message_surface = font_message.render(
                    current_line, True, message_color)
                screen.blit(message_surface, (x, y))
                y += font_message.get_height() + 5
                current_line = word

        # Renderizar la última línea
        if current_line:
            message_surface = font_message.render(
                current_line, True, message_color)
            screen.blit(message_surface, (x, y))
            y += font_message.get_height() + 20  # Espacio entre elementos


def flash_screen(screen: Surface, color: tuple, duration: int = 500, flashes: int = 3) -> None:
    """
    Hace que la pantalla parpadee con un color especifico.
    """

    interval = duration // (flashes * 2)
    for _ in range(flashes):
        screen.fill(color)
        pg.display.flip()
        pg.time.delay(interval)
        pg.display.flip()
        screen.fill((32, 32, 32))  # color original de fondo
        pg.display.flip()
        pg.time.delay(interval)


def pygame_blit_surface(screen: Surface, frame_surface,
                        window_width: int, window_height: int,
                        rotation_angle: int) -> None:
    """
    Aplica transformaciones a la superficie pygame, para luego pegarla en la pantalla
    """
    # Escalar la imagen para que ocupe todo el ancho de la pantalla
    target_w = window_width - (2 * BAR_SIZE)
    target_h = window_height

    # Escalar la imagen sin mantener la proporción
    frame_surface = pg.transform.scale(frame_surface, (target_w, target_h))

    # Aplicar rotación
    frame_surface = pg.transform.rotate(frame_surface, rotation_angle)

    # Calcular la posición para centrar la imagen
    if rotation_angle in [90, 270]:
        x_offset = (window_width - target_h) // 2
        y_offset = (window_height - target_w) // 2
    else:
        x_offset = (window_width - target_w) // 2
        y_offset = (window_height - target_h) // 2

    # Dibujar la imagen en la pantalla
    screen.blit(frame_surface, (x_offset, y_offset))


def draw_debug_menu(screen: Surface,
                    window_width: int, window_heigth: int,
                    rotation_angle: int) -> None:
    """
    Escribe textos del menu de debug
    """

    # Mostrar texto independiente de si estamos mostrando la camara
    draw_text(False, screen,
              f"Orientación: {args['orientation'].upper()}", 0, 0)

    # Mostrar la rotacion actual en base a la orientacion predeterminada
    draw_text(False, screen, f"Rotación actual: {rotation_angle}°", 0, 20)

    # Asistente actual
    draw_text(False, screen, f"Asistente actual: {args['assistant']}", 0, 40)

    # Modo demo
    draw_text(False, screen, f"Modo demostración: {args['demo']}", 0, 60)

    # Controles
    draw_text(False, screen, "<p>: tomar una foto", 0, window_heigth // 2)
    draw_text(False, screen, "<q>: cerrar programa",
              0, window_heigth // 2 + 20)
    draw_text(False, screen, "<s>: mostrar camara",
              0, window_heigth // 2 + 20*2)
    draw_text(False, screen, "<Esc>: fullscreen", 0, window_heigth // 2 + 20*3)
    draw_text(False, screen, "<Arrow Keys>: rotar",
              0, window_heigth // 2 + 20*4)


def scale_backgrounds(width: int, height: int) -> None:
    """
    Transforma las imagenes cargadas al tamaño definido por (width, height)
    """
    global notfound_nointernet
    global notfound_internet
    global found_nointernet
    global found_internet
    global background

    notfound_nointernet = pg.transform.scale(
        notfound_nointernet, (width, height))

    notfound_internet = pg.transform.scale(
        notfound_internet, (width, height))

    found_nointernet = pg.transform.scale(
        found_nointernet, (width, height))

    found_internet = pg.transform.scale(
        found_internet, (width, height))

    background = pg.transform.scale(background, (width, height))


def blit_background_to_screen(screen: Surface,
                              show_result: bool = False,
                              cam_found: bool = False,
                              inet_connection: bool = False) -> None:
    """
    Dibuja una imagen dependiendo de los booleanos
    """

    if show_result:
        screen.blit(background, (0, 0))
        return

    if not cam_found and not inet_connection:
        screen.blit(notfound_nointernet, (0, 0))

    elif not cam_found and inet_connection:
        screen.blit(notfound_internet, (0, 0))

    elif cam_found and not inet_connection:
        screen.blit(found_nointernet, (0, 0))

    else:
        screen.blit(found_internet, (0, 0))
