import os
import cv2
import numpy as np

def blur_score(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    lap = cv2.Laplacian(img, cv2.CV_64F)
    return lap.var()

orig_folder = os.path.join('motion_blur','dataset_Respuestas_estudiantes_PRAC','orig')
blur_folder = os.path.join('motion_blur','dataset_Respuestas_estudiantes_PRAC','blur')

original_vals = []
blurred_vals = []

# Calcular los valores de variacion del laplaciano
for name in os.listdir(blur_folder):
    path = os.path.join(blur_folder, name)
    if os.path.isfile(path):
        score = blur_score(path)
        blurred_vals.append(score)

for name in os.listdir(orig_folder):
    path = os.path.join(orig_folder, name)
    if os.path.isfile(path):
        score = blur_score(path)
        original_vals.append(score)

# Suponiendo que ya tienes las listas
lap_borroso = np.array(blurred_vals)
lap_nitido = np.array(original_vals)

# Resumen estadistico

print("BORROSAS")
print(f"Media: {lap_borroso.mean():.2f}")
print(f"Desviación estándar: {lap_borroso.std():.2f}")
print(f"Mediana: {np.median(lap_borroso):.2f}")

print("\nNÍTIDAS")
print(f"Media: {lap_nitido.mean():.2f}")
print(f"Desviación estándar: {lap_nitido.std():.2f}")
print(f"Mediana: {np.median(lap_nitido):.2f}")


# Calculo de threshold
print("\nUMBRAL")
threshold = (lap_borroso.mean() + lap_nitido.mean()) / 2
print(f"Umbral sugerido: {threshold:.2f}")
threshold_95 = np.percentile(lap_borroso, 95)
print(f"Umbral conservador (95% borrosas debajo): {threshold_95:.2f}")

def evaluar_threshold(threshold):
    pred_borrosas = lap_borroso > threshold  # Falsos negativos si True
    pred_nitidas = lap_nitido > threshold    # True = correctamente clasificadas como nítidas

    acc_borrosas = np.sum(~pred_borrosas) / len(lap_borroso)
    acc_nitidas = np.sum(pred_nitidas) / len(lap_nitido)
    acc_total = (np.sum(~pred_borrosas) + np.sum(pred_nitidas)) / (len(lap_borroso) + len(lap_nitido))

    print(f"\nEvaluando umbral = {threshold:.2f}")
    print(f"✔️ Precisión borrosas detectadas correctamente: {acc_borrosas*100:.2f}%")
    print(f"✔️ Precisión nítidas detectadas correctamente: {acc_nitidas*100:.2f}%")
    print(f"✔️ Precisión total: {acc_total*100:.2f}%")

evaluar_threshold(675.10)
evaluar_threshold(299.12)