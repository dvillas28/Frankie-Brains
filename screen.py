# screen.py
"""
Funciones que actuan sobre la pantalla
"""

import os
import pygame as pg
from pygame import Surface
from config import args

font = None

def initialize_font():
    """
    La font debe ser inicializada despues de ejecutar pg.init().
    """
    global font
    font = pg.font.SysFont("Consolas", 18)

def draw_text(always: bool, screen: Surface, text: str, x: int, y: int, color: tuple=(255,255,255)) -> None:
    """
    Dibuja texto en la pantalla en la posicion (x, y).
    """

    #  Si queremos mostrar el debug o si queremos mostrar el mensaje independiente de si estamos en debug o no
    if args["debug"] or always:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    return

def draw_wrapped_text(always: bool, screen: Surface, text: str, x: int, y: int, max_width: int, color: tuple=(255, 255, 255)) -> None:
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
    