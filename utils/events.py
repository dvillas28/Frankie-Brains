# events.py
"""
Manejo de eventos
"""

import pygame as pg


def handle_events(custom_events: dict, result_is_none: bool) -> tuple[bool, str]:
    """
    Manejo de eventos
    input: diccionario de eventos custom, si es que lo hay. Objeto de resultados
    return: bool que indica si el programa sigue corriendo y un string que indica la accion a tomar
    """

    for event in pg.event.get():

        # Quit events
        if event.type == pg.QUIT:
            return False, ''

        # Keydown events
        elif event.type == pg.KEYDOWN:
            return keydown_events(event, result_is_none)

        elif event.type == custom_events["photo_taken_Event"]:
            return True, 'photo_taken'

    return True, ''


photo_keys: set = {pg.K_0, pg.K_1}


def keydown_events(event, result_is_none: bool) -> tuple[bool, str]:
    """
    Manejo de eventos al presionar una tecla
    """

    global photo_keys

    # Salir al presionar q
    if event.key == pg.K_q:
        return False, ''

    # Si hay resultado y se presiona una de las teclas de imagen, limpiar resultado
    if (event.key in photo_keys) and result_is_none:
        return True, 'clear_result'

    elif event.key == pg.K_0:
        return True, 'try_to_take_photo:PLANIFICACION'

    elif event.key == pg.K_1:
        return True, 'try_to_take_photo:REVISION'

    # fullscreen al presionar escape
    elif event.key == pg.K_ESCAPE:
        return True, 'toggle_fullscreen'

    elif event.key == pg.K_s:
        return True, 'toggle_camera'

    elif event.key == pg.K_d:
        return True, 'toggle_debug_menu'

    elif event.key == pg.K_LEFT:
        return True, 'rotate_left'

    elif event.key == pg.K_RIGHT:
        return True, 'rotate_right'

    return True, ''
