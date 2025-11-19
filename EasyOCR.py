import easyocr
import cv2
import os
import re
import numpy as np

# Crear lector OCR
reader = easyocr.Reader(['es', 'en'])

CARPETA_IMAGENES = "imagen"
EXTS = (".jpg", ".jpeg", ".png")

# -----------------------------
# FUNCIONES PARA EXTRAER DATOS
# -----------------------------

def extraer_placa(texto):
    patron = r"\b([A-Z]{3}[0-9]{3}|[A-Z]{3}[0-9]{2}[A-Z])\b"
    match = re.search(patron, texto)
    return match.group(0) if match else None

def extraer_cedula(texto):
    patron = r"\b\d{6,12}\b"
    matches = re.findall(patron, texto)
    if matches:
        return matches[-1]   # usualmente la última es la cédula
    return None

def extraer_nombre(texto):
    patron = r"\b[A-ZÁÉÍÓÚÑ ]{10,}\b"
    matches = re.findall(patron, texto)
    if matches:
        # filtramos palabras muy generales
        prohibidas = ["REPUBLICA", "MINISTERIO", "COLOMBIA", "TRANSPORTE"]
        nombres = [m for m in matches if not any(p in m for p in prohibidas)]
        if nombres:
            return nombres[-1]
    return None


# -----------------------------
# RECORRER IMÁGENES
# -----------------------------
for archivo in os.listdir(CARPETA_IMAGENES):

    if not archivo.lower().endswith(EXTS):
        continue

    ruta = os.path.join(CARPETA_IMAGENES, archivo)
    print(f"\n📸 Procesando: {archivo}")

    # OCR
    resultados = reader.readtext(ruta, detail=1, paragraph=False)

    # Convertir a un texto completo
    texto_completo = " ".join([res[1].upper() for res in resultados])

    # -------- EXTRAER DATOS --------
    placa = extraer_placa(texto_completo)
    cedula = extraer_cedula(texto_completo)
    nombre = extraer_nombre(texto_completo)
    
    
    

    print("🟦 Datos detectados:")
    print("   ➤ Placa:", placa)
    print("   ➤ Nombre:", nombre)
    print("   ➤ Cédula:", cedula)

    # -------- GUARDAR EN TXT --------
    nombre_txt = archivo.rsplit(".", 1)[0] + "_OCR.txt"
    ruta_txt = os.path.join(CARPETA_IMAGENES, nombre_txt)

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(f"PLACA: {placa}\n")
        f.write(f"NOMBRE: {nombre}\n")
        f.write(f"CEDULA: {cedula}\n\n")
        f.write("TEXTO COMPLETO OCR:\n")
        f.write(texto_completo)

    print("📝 Guardado:", ruta_txt)

    # -------- MOSTRAR EN VENTANA --------
    img = cv2.imread(ruta)
    h, w = img.shape[:2]

    panel = 255 * np.ones((h + 150, w, 3), dtype=np.uint8)
    panel[0:h, 0:w] = img

    cv2.putText(panel, f"Placa: {placa}", (20, h + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.putText(panel, f"Propietario: {nombre}", (20, h + 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.putText(panel, f"Cedula: {cedula}", (20, h + 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("Datos extraídos", panel)
    cv2.waitKey(0)

cv2.destroyAllWindows()
print("\n✅ OCR finalizado.")
