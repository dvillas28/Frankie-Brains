import pygame
import cv2
import sys
import os
import argparse
from datetime import datetime
from detect_blur import check_blur

# Parser de argumentos por consola
ap = argparse.ArgumentParser()

# Argumento para especificar la calidad del video
ap.add_argument("-q", "--quality",
                required=False,
                help="Parametro de calidad de la camara. Low: 0, High: 1. Valor default: 0",
                choices=["0", "1"],
                default="0")

# Se asume que la camara esta en orientacion norte por defecto
ap.add_argument("-o", "--orientation",
                required=False,
                help="Parametro de orientación de la camara. Valor default: n (norte)",
                choices=["n", "o", "s", "e"],
                default="n",
                type=str.lower)

# Argumento para mostrar la camara
ap.add_argument("-s", "--show",
                required=False,
                help="Mostrar camara. Valor default: False",
                action="store_true")

args = vars(ap.parse_args())

# Inicializar pygame
pygame.init()

# Buscar una cámara conectada
def find_camera(start_range=0):
    if os.name == 'nt':
        start_range = 1 # saltarse la camara de defecto
    
    ranges = (start_range,10)
    for i in range(*ranges):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None

# Pantalla principal en modo fullscreen
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SCALED)
# screen = pygame.display.set_mode((800, 600))  # Resolución fija para pruebas
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
fullscreen = True

font = pygame.font.SysFont("Consolas", 18)

def draw_text(text, x, y, color=(255,255,255)):
    """Dibuja texto en la pantalla en la posicion (x, y)"""

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_wrapped_text(text, x, y, max_width, color=(255, 255, 255)):
    """Dibuja texto en la pantalla con ajuste de línea (wrap) si es demasiado largo."""
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

filepath = ''
is_blurry = ''
def take_photo(frame):
    global filepath
    global is_blurry
    abspath = os.path.dirname(os.path.realpath(__file__))
    pics_dir = os.path.join(abspath, "pics")
    os.makedirs(pics_dir, exist_ok=True)

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
    frame = cv2.flip(frame, 0)
        
    now = datetime.now()
    filename = now.strftime("%Y_%m_%d-%H-%M-%S") + ".jpg"
    filepath = os.path.join(pics_dir, filename)

    cv2.imwrite(filepath, frame)
    print(f"Foto guardada en: {filepath}")

    is_blurry = check_blur(filepath)

def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
    else:
        # screen = pygame.display.set_mode((1280, 720))
        screen = pygame.display.set_mode((800, 600))
        pygame.mouse.set_visible(True)

def set_rotation_angle():
    """
    Rotar el video en funcion de la orientacion actual de la camara
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

# Loop principal
running = True
camera_found = False
cap = None

photo_taken_Event = pygame.USEREVENT + 1
photo_taken = False

rotation_angle = set_rotation_angle()

while running:
    if not camera_found:
        camera_index = find_camera()
        if camera_index is not None:
            cap = cv2.VideoCapture(camera_index)
            
            quality = int(args["quality"])
                
            if quality:

                # Resolucion de alta calidad
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            else:
            
                # Resolucion de baja calidad
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Configurar resolución
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Usar MJPEG
            # cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Ajustar brillo
            # cap.set(cv2.CAP_PROP_CONTRAST, 0.5)    # Ajustar contraste
            # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # Habilitar exposición automática
            camera_found = True

    screen.fill((32,32,32))

    if camera_found and cap is not None:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame) # corregir rotacion si es que
            frame_surface = pygame.surfarray.make_surface(frame)

            # Ajustar tamaño para que la imagen ocupe todo el ancho de la pantalla
            frame_h, frame_w = frame.shape[:2]
            win_w, win_h = screen.get_size()

            if args["show"]:
                # Escalar la imagen para que ocupe todo el ancho de la pantalla
                bar_size = 250
                target_w = win_w - (2 * bar_size)
                target_h = win_h

                # Escalar la imagen sin mantener la proporción
                frame_surface = pygame.transform.scale(frame_surface, (target_w, target_h))

                # Aplicar rotación
                frame_surface = pygame.transform.rotate(frame_surface, rotation_angle)

                # Calcular la posición para centrar la imagen
                if rotation_angle in [90, 270]:
                    x_offset = (win_w - target_h) // 2
                    y_offset = (win_h - target_w) // 2
                else:
                    x_offset = (win_w - target_w) // 2
                    y_offset = (win_h - target_h) // 2

                # Dibujar la imagen en la pantalla
                screen.blit(frame_surface, (x_offset, y_offset))

            # Mostrar texto en los bordes grises
            # Mostrar la orientación predeterminada ingresada en consola
            default_orientation_text = f"Orientación: {args['orientation'].upper()}"
            draw_text(default_orientation_text, 0, 0)

            # Mostrar la rotacion actual en base a la orientacion predeterminada
            rotation_angle_text = f"Rotación actual: {rotation_angle}°"
            draw_text(rotation_angle_text, 0, 20)
            
            # Controles
            draw_text("<p>: tomar una foto", 0, win_h // 2)
            draw_text("<q>: cerrar programa", 0, win_h // 2 + 20)
            draw_text("<Esc>: fullscreen", 0, win_h // 2 + 20*2)
            draw_text("<Arrow Keys>: rotar", 0, win_h // 2 + 20*3)
            
        if photo_taken:
            draw_wrapped_text(f"Foto guardada en: {filepath}", win_w - 500, win_h // 2, 250)            
            draw_text(f"Borrosa?: {is_blurry}", 0, win_h // 2 + 20*4)            

    else:
        draw_text("Buscando cámara...", screen_width // 2 - 150, screen_height // 2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_q:
                running = False
            
            elif event.key == pygame.K_p and camera_found:
                take_photo(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                photo_taken = True
                pygame.time.set_timer(photo_taken_Event, 5000)

            # Pantalla completa
            elif event.key == pygame.K_ESCAPE:
                toggle_fullscreen()

            # Rotaciones de imagen
            elif event.key == pygame.K_LEFT:
                rotation_angle = (rotation_angle - 90) % 360 # 90° a la izquierda

            elif event.key == pygame.K_RIGHT:
                rotation_angle = (rotation_angle + 90) % 360 # 90° a la derecha

        if event.type == photo_taken_Event:
            pygame.time.set_timer(photo_taken_Event, 0)
            photo_taken = False

    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

if cap:
    cap.release()
pygame.quit()
