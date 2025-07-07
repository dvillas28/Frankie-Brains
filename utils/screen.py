# screen.py
"""
Funciones que actuan sobre la pantalla
"""

import os
import pygame as pg
from pygame import Surface
from utils.config import args, BAR_SIZE, COLOR_BLACK, DEBUG_FONT, RESULTS_FONT

font = None

def initialize_font():
    """
    La font debe ser inicializada despues de ejecutar pg.init().
    """
    global font
    font = pg.font.SysFont(DEBUG_FONT, 18)

def draw_text(always: bool, screen: Surface, text: str, x: int, y: int, color: tuple=COLOR_BLACK) -> None:
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

def draw_list_items(screen: Surface, items: list, rect: pg.Rect, font_size: int, title_color: tuple, message_color: tuple) -> None:
    """
    Dibuja una lista de elementos (título y mensaje) dentro de un rectángulo en la pantalla.
    """
    font_title = pg.font.SysFont(RESULTS_FONT, font_size)
    font_message = pg.font.SysFont(RESULTS_FONT, font_size - 4)  # Mensaje con fuente más pequeña

    # Margen interno dentro del rectángulo
    padding = 20
    x, y = rect.x + padding, rect.y + padding

    max_width = rect.width - (2 * padding) # ancho máximo

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
                message_surface = font_message.render(current_line, True, message_color)
                screen.blit(message_surface, (x, y))
                y += font_message.get_height() + 5
                current_line = word

        # Renderizar la última línea
        if current_line:
            message_surface = font_message.render(current_line, True, message_color)
            screen.blit(message_surface, (x, y))
            y += font_message.get_height() + 20  # Espacio entre elementos

def draw_wrapped_text(always: bool, screen: Surface, text: str, x: int, y: int, max_width: int, color: tuple=COLOR_BLACK) -> None:
    """
    Dibuja texto en la pantalla con ajuste de línea (wrap) si es demasiado largo.
    """
    
    #  Si queremos mostrar el debug o si queremos mostrar el mensaje independiente de si estamos en debug o no
    if args["debug"] or always:
        sep = lambda: '\\' if os.name == 'nt' else '/'
        words = text.split(sep())
        lines = []
        current_line = ""

        for word in words:
            # Probar si agregar la palabra excede el ancho máximo
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        # Agregar la última línea
        if current_line:
            lines.append(current_line)

        # Dibujar cada línea
        line_height = font.size("Tg")[1]  # Altura de una línea de texto
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x, y + i * line_height))

    return

def flash_screen(screen: Surface, color: tuple, duration: int=500, flashes: int=3) -> None:
    """
    Hace que la pantalla parpadee con un color especifico.
    """

    interval = duration // (flashes * 2)
    for _ in range(flashes):
        screen.fill(color)
        pg.display.flip()
        pg.time.delay(interval)
        pg.display.flip()
        screen.fill((32, 32, 32)) # color original de fondo
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
    draw_text(False, screen, f"Orientación: {args['orientation'].upper()}", 0, 0)

    # Mostrar la rotacion actual en base a la orientacion predeterminada
    draw_text(False, screen, f"Rotación actual: {rotation_angle}°", 0, 20)
                
    # Controles
    draw_text(False, screen, "<p>: tomar una foto", 0, window_heigth // 2)
    draw_text(False, screen, "<q>: cerrar programa", 0, window_heigth // 2 + 20)
    draw_text(False, screen, "<s>: mostrar camara", 0, window_heigth // 2 + 20*2)
    draw_text(False, screen, "<Esc>: fullscreen", 0, window_heigth // 2 + 20*3)
    draw_text(False, screen, "<Arrow Keys>: rotar", 0, window_heigth // 2 + 20*4)
