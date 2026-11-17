
"""Guardado seguro de archivos Markdown."""

from pathlib import Path


def guardar_markdown(nombre_archivo, contenido):
    """Guarda contenido dentro de salida/ de forma segura."""

    # 1. Validar el nombre
    if not isinstance(nombre_archivo, str) or not nombre_archivo:
        return {"ok": False, "error": "El nombre del archivo no puede estar vacío"}

    if not nombre_archivo.endswith(".md"):
        return {"ok": False, "error": "El archivo debe terminar en .md"}

    if (
        Path(nombre_archivo).is_absolute()
        or Path(nombre_archivo).name != nombre_archivo
        or "\\" in nombre_archivo
    ):
        return {"ok": False, "error": "Solo se permiten nombres de archivo, sin rutas"}

    # 2. Construir las rutas
    carpeta = Path("salida")
    ruta = carpeta / nombre_archivo
    temporal = carpeta / (nombre_archivo + ".tmp")

    try:
        # 3. Crear la carpeta si no existe
        carpeta.mkdir(parents=True, exist_ok=True)

        # 4. Escribir primero en el archivo temporal
        temporal.write_text(contenido, encoding="utf-8")

        # 5. Reemplazar el destino cuando la escritura terminó
        temporal.replace(ruta)

        return {
            "ok": True,
            "ruta": str(ruta)
        }

    except Exception as error:
        # 6. Eliminar el temporal si ocurrió un error
        try:
            temporal.unlink(missing_ok=True)
        except OSError:
            pass

        return {
            "ok": False,
            "error": str(error)
        }
