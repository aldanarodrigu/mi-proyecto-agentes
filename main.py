"""Aplicación principal: coordina el flujo secuencial de agentes."""

import re
import unicodedata

from agentes.disenador_practica import crear_agente_disenador
from agentes.explicador import crear_agente_explicador
from agentes.revisor import crear_agente_revisor
from herramientas.archivos import guardar_markdown
from herramientas.validacion import validar_guia
from runtime.ejecutor import ejecutar_agente
from runtime.errores import (
    ConfiguracionIncompleta,
    ErrorDeArchivo,
    LimiteTemporal,
    ProveedorNoAdmitido,
    RespuestaVacia,
    ServicioNoDisponible,
)


def _nombre_archivo(tema):
    """Convierte el tema en un nombre de archivo Markdown seguro."""
    texto = unicodedata.normalize("NFKD", tema).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-") or "guia"
    return f"guia-{slug}.md"


def _construir_borrador(tema, explicacion, practica):
    """Arma el borrador con las respuestas completas de los agentes."""
    return (
        f"# Guía de estudio: {tema}\n\n"
        f"## Explicación\n\n{explicacion.strip()}\n\n"
        f"## Práctica\n\n{practica.strip()}\n"
    )


def ejecutar_flujo(tema, ejecutar=ejecutar_agente, permitir_correccion=False):
    """Coordina los agentes usando un ejecutor reemplazable en las pruebas.

    tema → explicador → diseñador → borrador → revisor
         → guía final → validación → archivo Markdown
    """
    if not isinstance(tema, str) or not tema.strip():
        raise ValueError("El tema no puede estar vacío.")
    tema = tema.strip()

    explicacion = ejecutar(
        crear_agente_explicador(),
        f"Explica el tema de Python: {tema}",
    )

    practica = ejecutar(
        crear_agente_disenador(),
        f"Tema: {tema}\n\nExplicación previa:\n\n{explicacion}",
    )

    borrador = _construir_borrador(tema, explicacion, practica)

    revisor = crear_agente_revisor()
    guia_final = ejecutar(revisor, borrador)

    validacion = validar_guia(guia_final)

    if not validacion["valida"] and permitir_correccion:
        mensaje_correccion = (
            "La guía revisada no cumple los requisitos. "
            f"Faltan: {', '.join(validacion['faltantes'])}.\n"
            f"Debe comenzar con «# Guía de estudio: {tema}» e incluir "
            "## Explicación, ## Práctica, ## Revisión y un bloque ```python.\n\n"
            f"Guía a corregir:\n\n{guia_final}"
        )
        guia_final = ejecutar(revisor, mensaje_correccion)
        validacion = validar_guia(guia_final)

    if not validacion["valida"]:
        return {"ok": False, "faltantes": validacion["faltantes"]}

    guardado = guardar_markdown(_nombre_archivo(tema), guia_final)
    if not guardado["ok"]:
        raise ErrorDeArchivo(guardado["error"])
    return {"ok": True, "ruta": guardado["ruta"]}


def main():
    tema = input("Tema de Python: ").strip()
    try:
        resultado = ejecutar_flujo(tema)
    except ValueError as error:
        print(f"Error: {error}")
        return 1
    except (ConfiguracionIncompleta, ProveedorNoAdmitido) as error:
        print(f"Error de configuración: {error} Revisa el archivo .env.")
        return 1
    except LimiteTemporal as error:
        print(f"Límite de uso: {error} No se realizaron más llamadas.")
        return 1
    except ServicioNoDisponible as error:
        print(
            f"Servicio no disponible: {error} Espera al menos un minuto y vuelve "
            "a ejecutar el comando una sola vez; si persiste, registra el modelo, "
            "la hora y el mensaje, y consulta https://aistudio.google.com/status."
        )
        return 1
    except RespuestaVacia as error:
        print(f"Respuesta vacía: {error} No se guardó ninguna guía.")
        return 1
    except ErrorDeArchivo as error:
        print(f"Error al guardar: {error} No se guardó contenido parcial.")
        return 1

    if not resultado["ok"]:
        print(
            "La guía no es válida y no se guardó. Faltan: "
            + ", ".join(resultado["faltantes"])
        )
        return 1
    print(f"Guía guardada en: {resultado['ruta']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
