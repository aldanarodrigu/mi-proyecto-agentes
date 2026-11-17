from pathlib import Path

import pytest

import main
from runtime.errores import (
    ConfiguracionIncompleta,
    LimiteTemporal,
    RespuestaVacia,
    ServicioNoDisponible,
)

CLAVE = "AIzaClaveDePruebaQueNoDebeAparecer123"

GUIA_VALIDA = """# Guía de estudio: listas

## Explicación

```python
print(1)
```

## Práctica

Ejercicio.

## Revisión

- Sin cambios.
"""


@pytest.fixture(autouse=True)
def entorno(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_MODEL", "modelo-local-para-pruebas")
    monkeypatch.setenv("GOOGLE_API_KEY", CLAVE)
    monkeypatch.chdir(tmp_path)


def _ejecutar_main(monkeypatch, tema, ejecutar):
    monkeypatch.setattr("builtins.input", lambda _: tema)
    original = main.ejecutar_flujo
    monkeypatch.setattr(
        main, "ejecutar_flujo", lambda t: original(t, ejecutar=ejecutar)
    )
    return main.main()


def _sin_secretos(salida):
    assert CLAVE not in salida
    assert CLAVE[:8] not in salida and CLAVE[-8:] not in salida


def test_tema_vacio(monkeypatch, capsys):
    codigo = _ejecutar_main(monkeypatch, "   ", lambda a, m: pytest.fail("no"))
    assert codigo == 1
    assert "vacío" in capsys.readouterr().out


@pytest.mark.parametrize(
    "error, texto",
    [
        (ConfiguracionIncompleta("Falta configurar: GEMINI_MODEL."), "configuración"),
        (LimiteTemporal("Se alcanzó un límite temporal."), "Límite"),
        (ServicioNoDisponible("El servicio no está disponible."), "no disponible"),
        (RespuestaVacia("Sin texto."), "vacía"),
    ],
)
def test_errores_del_ejecutor_sin_reintento(monkeypatch, capsys, tmp_path, error, texto):
    llamadas = []

    def ejecutar_falla(agente, mensaje):
        llamadas.append(agente.name)
        raise error

    codigo = _ejecutar_main(monkeypatch, "listas", ejecutar_falla)
    salida = capsys.readouterr().out
    assert codigo == 1
    assert len(llamadas) == 1
    assert texto in salida
    _sin_secretos(salida)
    assert not (tmp_path / "salida").exists()


def test_guia_invalida_no_se_guarda(monkeypatch, capsys, tmp_path):
    codigo = _ejecutar_main(monkeypatch, "listas", lambda a, m: "guía incompleta")
    salida = capsys.readouterr().out
    assert codigo == 1
    assert "Faltan" in salida
    assert not (tmp_path / "salida").exists()


def test_guia_con_clave_no_se_guarda(monkeypatch, capsys, tmp_path):
    codigo = _ejecutar_main(
        monkeypatch, "listas", lambda a, m: GUIA_VALIDA + f"\n{CLAVE}\n"
    )
    salida = capsys.readouterr().out
    assert codigo == 1
    assert "contenido sensible" in salida
    _sin_secretos(salida)
    assert not (tmp_path / "salida").exists()


def test_fallo_de_escritura_no_deja_contenido_parcial(monkeypatch, capsys, tmp_path):
    def escritura_falla(self, *args, **kwargs):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(Path, "write_text", escritura_falla)
    codigo = _ejecutar_main(monkeypatch, "listas", lambda a, m: GUIA_VALIDA)
    salida = capsys.readouterr().out
    assert codigo == 1
    assert "Error al guardar" in salida
    assert list((tmp_path / "salida").iterdir()) == []
