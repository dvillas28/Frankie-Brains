import numpy as np
import cv2
import random
import os

def motion_blur(img, size=15, angle=0):
    """
    Funcion que aplica motion blur a una img
    """
    kernel = np.zeros((size, size))
    kernel[(size - 1) // 2, :] = np.ones(size)
    
    # Rotar el kernel para simular diferentes direcciones
    M = cv2.getRotationMatrix2D((size / 2, size / 2), angle, 1)
    kernel = cv2.warpAffine(kernel, M, (size, size))
    kernel /= kernel.sum()
    
    return cv2.filter2D(img, -1, kernel)

orig_folder = os.path.join('motion_blur','dataset_Respuestas_estudiantes_PRAC','orig')
blur_folder = os.path.join('motion_blur','dataset_Respuestas_estudiantes_PRAC','blur')
os.makedirs(blur_folder, exist_ok=True)


for filename in os.listdir(orig_folder):
    # suponemos que todas las imagenes terminan con .jpg

    img_path = os.path.join(orig_folder, filename)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Unos parametros aleatorios
    size = random.choice([9, 15, 21, 25, 31])
    angle = random.uniform(-45,45)

    blurred = motion_blur(img, size=size, angle=angle)

    output_path = os.path.join(blur_folder, f"blur_{size}_{int(angle)}_{filename}")
    cv2.imwrite(output_path, blurred)

