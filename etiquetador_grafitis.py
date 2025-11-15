import cv2
import os
import pandas as pd
from PIL import Image
from datetime import datetime
import json

# ==========================
# CARGA DE CONFIGURACIÓN
# ==========================
CONFIG_FILE = "config.json"

if not os.path.isfile(CONFIG_FILE):
    raise FileNotFoundError(
        f"No se encontró {CONFIG_FILE}. Crea un archivo config.json siguiendo el ejemplo."
    )

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

carpeta_imagenes = config["input_images"]
carpeta_recortes = config["output_crops"]
csv_base = config["input_csv"]

# Crear carpeta de salida si no existe
os.makedirs(carpeta_recortes, exist_ok=True)

# Cargar CSV
df_base = pd.read_csv(csv_base, encoding='utf-8', sep=';')
df_base.columns = df_base.columns.str.strip()
print("Columnas detectadas:", df_base.columns.tolist())

datos_etiquetados = []

# ==========================
# VARIABLES DE CONTROL
# ==========================
drawing = False
x_start, y_start = -1, -1
img_original = None
img_display = None
img_name = ""
img_counter = 0
indice_actual = 0

mapa_tipos = {
    '1': 'firma',
    '2': 'pieza',
    '3': 'dibujo',
    '4': 'frase',
    '5': 'otro'
}

# ==========================
# EVENTOS RATÓN
# ==========================
def dibujar_rectangulo(event, x, y, flags, param):
    global x_start, y_start, drawing, img_display

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_display = img_original.copy()
        cv2.rectangle(img_display, (x_start, y_start), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y
        img_display = img_original.copy()
        cv2.rectangle(img_display, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        tipo = seleccionar_tipo()
        if tipo is not None:
            guardar_recorte(x_start, y_start, x_end, y_end, tipo)
        else:
            print("❌ Recorte cancelado.")

# ==========================
# SELECCIÓN DEL TIPO
# ==========================
def seleccionar_tipo():
    print("\nSelecciona tipo:")
    print("1 Firma | 2 Pieza | 3 Dibujo | 4 Frase | 5 Otro | C Cancelar")
    while True:
        tecla = cv2.waitKey(0) & 0xFF
        if chr(tecla) in mapa_tipos:
            return mapa_tipos[chr(tecla)]
        if tecla in [ord('c'), ord('C')]:
            return None
        print("❗ Pulsa 1-5 o C")

# ==========================
# GUARDAR RECORTE
# ==========================
def guardar_recorte(x1, y1, x2, y2, tipo):
    global img_counter, img_name, img_original, datos_etiquetados, indice_actual

    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    recorte = img_original[y1:y2, x1:x2]

    fila = df_base.iloc[indice_actual]
    ID = int(fila["ID"])
    X = int(fila["X"])
    Y = int(fila["Y"])

    nombre_base = os.path.splitext(img_name)[0]
    nombre_sin_prefijo = nombre_base.replace("puntos-1_", "")

    nombre_recorte = f"{nombre_sin_prefijo}_{img_counter}_{tipo}_{X}_{Y}.jpg"
    ruta_recorte = os.path.join(carpeta_recortes, nombre_recorte)
    cv2.imwrite(ruta_recorte, recorte)

    print(f"✅ Guardado: {nombre_recorte}")

    datos_etiquetados.append({
        "ID": ID,
        "recorte_nombre": nombre_recorte,
        "tipo": tipo,
        "X": X,
        "Y": Y
    })

    img_counter += 1

# ==========================
# BUCLE PRINCIPAL
# ==========================
while 0 <= indice_actual < len(df_base):

    fila = df_base.iloc[indice_actual]
    img_name = fila["Fotografía"].strip()

    ruta_img = os.path.join(carpeta_imagenes, img_name)
    if not os.path.isfile(ruta_img):
        print(f"⚠️ Imagen no encontrada: {ruta_img}")
        indice_actual += 1
        continue

    img_original = cv2.imread(ruta_img)
    img_display = img_original.copy()
    img_counter = 1

    cv2.namedWindow("Imagen", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Imagen", 1000, 800)
    cv2.setMouseCallback("Imagen", dibujar_rectangulo)

    print(f"\n🖼️ Imagen {indice_actual+1}/{len(df_base)}: {img_name}")
    print("👉 N siguiente | B volver | ESC salir")
    print("👉 Selecciona con ratón + 1-5 | C cancelar")

    while True:
        cv2.imshow("Imagen", img_display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('n'):
            indice_actual += 1
            break
        elif key == ord('b'):
            indice_actual = max(0, indice_actual - 1)
            break
        elif key == 27:
            indice_actual = len(df_base)
            break

    cv2.destroyAllWindows()

# ==========================
# GUARDAR RESULTADOS
# ==========================
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
nombre_salida = f"etiquetas_grafitis_{timestamp}.xlsx"
df_salida = pd.DataFrame(datos_etiquetados)
df_salida.to_excel(nombre_salida, index=False)

print(f"\n✅ Datos guardados correctamente en: {nombre_salida}")
print("✅ Proceso completado")
