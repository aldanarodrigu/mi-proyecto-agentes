"""Validación determinista de guías de estudio."""

import os


def validar_guia(contenido):

    if not contenido or not contenido.strip():
        return {"valida": False, "faltantes": ["contenido no vacío"]}

    faltantes = []

    if not contenido.startswith("# Guía de estudio:"):
        faltantes.append("título")


    if "## Explicación" not in contenido:
        faltantes.append("## Explicación")

    if "## Práctica" not in contenido:
        faltantes.append("## Práctica")

    if "## Revisión" not in contenido:
        faltantes.append("## Revisión")

    if "```python" not in contenido:
        faltantes.append("bloque de código Python")

    clave = os.getenv("GOOGLE_API_KEY")

    if "TRAINING_SECRET_TEST_VALUE" in contenido or (
        clave and clave in contenido
    ):
        faltantes.append("contenido sensible")

    return {
        "valida": not faltantes,
        "faltantes": faltantes
    }