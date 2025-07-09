# events.py

"""
Manejo de eventos
"""

import pygame as pg

def handle_events(custom_events: dict, result: dict) -> tuple[bool, str]:
    """
    Manejo de eventos
    input: diccionario de eventos custom, si es que lo hay
    return: bool que indica si el programa sigue corriendo y un string que indica la accion a tomar
    """

    for event in pg.event.get():

        # Quit events
        if event.type == pg.QUIT:
            return False, ''
        
        # Keydown events
        elif event.type == pg.KEYDOWN:
            return keydown_events(event, result)
        
        elif event.type == custom_events["photo_taken_Event"]:
            return True, 'photo_taken'
        
    return True, ''

    

def keydown_events(event, result: dict) -> tuple[bool, str]:
    """
    Manejo de eventos al presionar una tecla
    """
    
    # Salir al presionar q
    if event.key == pg.K_q:
        return False, ''
    
    # Si hay resultado y se presiona p, limpiar resultado
    if event.key == pg.K_p and result:
        return True, 'clear_result'

    # probar a tomar una foto al presionar q
    elif event.key == pg.K_p:
        return True, 'try_to_take_photo'
    
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