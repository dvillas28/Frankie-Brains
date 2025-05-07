# detect_blur.py
"""
Funciones para analizar borrosidad de una imagen
"""
import cv2

THRESHOLD = 299.12

def variance_of_laplacian(image):
    """
    Calcular el Laplaciano de la imagen y retorna el 'focus measure', 
    que es la variacion del laplaciano
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()

def check_blur(image_path: str) -> bool:
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	var_lap = variance_of_laplacian(gray)

	blur = False
      
	if var_lap < THRESHOLD:
		blur = True

	print(f"Blurriness value: {var_lap}. Blur {blur}")

	return blur