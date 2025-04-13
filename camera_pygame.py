import pygame
import cv2
import sys
import os
from datetime import datetime

# Inicializar pygame
pygame.init()

# Buscar una cámara conectada
def find_camera():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None

# Configuración inicial
camera_index = find_camera()
while camera_index is None:
    print("No se encontró cámara.")
    camera_index = find_camera()

    #sys.exit()

cap = cv2.VideoCapture(camera_index)

# Reducimos resolución para mejor rendimiento
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Pantalla principal en modo fullscreen
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

clock = pygame.time.Clock()
fullscreen = True

def take_photo(frame):
    abspath = os.path.dirname(os.path.realpath(__file__))
    pics_dir = os.path.join(abspath, "pics")
    os.makedirs(pics_dir, exist_ok=True)

    now = datetime.now()
    filename = now.strftime("%Y_%m_%d-%H-%M-%S") + ".jpg"
    filepath = os.path.join(pics_dir, filename)

    cv2.imwrite(filepath, frame)
    print(f"Foto guardada en: {filepath}")

def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1280, 720))

# Loop principal
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)  # Corregir rotación si es necesario
    frame_surface = pygame.surfarray.make_surface(frame)

    # Ajustar tamaño manteniendo la proporción
    frame_h, frame_w = frame.shape[:2]
    win_w, win_h = screen.get_size()

    ratio = frame_w / frame_h
    target_w = win_w
    target_h = int(win_w / ratio)
    if target_h > win_h:
        target_h = win_h
        target_w = int(win_h * ratio)

    frame_surface = pygame.transform.scale(frame_surface, (target_w, target_h))

    # Rellenar fondo negro y centrar imagen
    screen.fill((0, 0, 0))
    screen.blit(frame_surface, ((win_w - target_w) // 2, (win_h - target_h) // 2))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                take_photo(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            elif event.key == pygame.K_ESCAPE:
                toggle_fullscreen()

    clock.tick(30)  # Limitar a 30 FPS

cap.release()
pygame.quit()
