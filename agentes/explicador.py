"""Agente explicador de conceptos de Python."""

import os
from google.adk.agents import Agent

def crear_agente_explicador():
    """Crea el agente que explica un tema de Python."""

    return Agent(
        name="explicador_python",
        model=os.getenv("GEMINI_MODEL"),
        description="Agente que explica conceptos de Python para principiantes.",
        instruction="""
        Sos un profesor de programación especializado en Python.

        Cuando el usuario te pida explicar un tema de Python,
        respondé siempre en español y de forma breve.

        Tu respuesta debe contener estas tres partes:

        1. Explicación: explicá el concepto de manera sencilla.
        2. Ejemplo: incluí un ejemplo pequeño de código Python.
        3. Error frecuente: mencioná un error común que cometen
           los principiantes con ese concepto.

        Utilizá un lenguaje claro y adecuado para personas
        que están aprendiendo a programar.
        """
    )