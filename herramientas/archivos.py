
"""Guardado seguro de archivos Markdown."""

from pathlib import Path


def guardar_markdown(nombre_archivo, contenido):
    """Guarda contenido dentro de salida/ de forma segura."""

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

    carpeta = Path("salida")
    ruta = carpeta / nombre_archivo
    temporal = carpeta / (nombre_archivo + ".tmp")

    try:
        carpeta.mkdir(parents=True, exist_ok=True)

        temporal.write_text(contenido, encoding="utf-8")

        temporal.replace(ruta)

        return {
            "ok": True,
            "ruta": str(ruta)
        }

    except OSError as error:
        try:
            temporal.unlink(missing_ok=True)
        except OSError:
            pass

        motivo = error.strerror or error.__class__.__name__
        return {
            "ok": False,
            "error": f"No fue posible escribir {ruta}: {motivo}."
        }
