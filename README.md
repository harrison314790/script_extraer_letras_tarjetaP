# Script: Extraer texto de tarjeta de propiedad con EasyOCR 

Descripción
- Proyecto pequeño en Python que recorre la carpeta `imagen/`, aplica OCR con EasyOCR y extrae datos útiles (placa, cédula, nombre). Para cada imagen crea un archivo de texto con sufijo `_OCR.txt` dentro de la misma carpeta y muestra una vista con los datos sobre la imagen usando OpenCV.

¿Qué hace el script?
- Lee todas las imágenes (`.jpg`, `.jpeg`, `.png`) dentro de la carpeta `imagen/`.
- Ejecuta OCR con `easyocr.Reader(['es','en'])`.
- Normaliza el texto y aplica expresiones regulares para extraer:
  - Placa (formato típico de placas)
  - Cédula (números de 6 a 12 dígitos)
  - Nombre (bloques de texto en mayúsculas)
- Guarda un fichero por imagen con el texto extraído y el OCR completo (`<imagen>_OCR.txt`).
- Abre una ventana con OpenCV mostrando la imagen y los datos extraídos.

Requisitos
- Python 3.8+ (recomendado)
- Paquetes (instalar con pip):

```powershell
pip install easyocr opencv-python-headless numpy
```

Nota: si quieres ver la ventana de OpenCV en Windows instala `opencv-python` en lugar de `opencv-python-headless`:

```powershell
pip install easyocr opencv-python numpy
```

Uso
1. Coloca las imágenes dentro de la carpeta `imagen/`.
2. Ejecuta el script desde la raíz del proyecto:

```powershell
python EasyOCR.py
```

3. Para cada imagen se creará `imagen/<nombre>_OCR.txt` con los datos extraídos y el texto OCR completo.

Limitaciones y recomendaciones
- El script usa expresiones regulares simples; puede fallar con formatos inusuales o texto muy ruidoso.
- Para mejorar resultados, prueba preprocesar imágenes (ajustar contraste, binarizar, recortar).
- Si vas a procesar muchas imágenes sin mostrar ventanas, comenta o elimina la parte que usa `cv2.imshow` para evitar que el proceso se detenga por cada imagen.



Licencia
- Uso personal / educativo. Añade la tuya si lo vas a compartir públicamente.
