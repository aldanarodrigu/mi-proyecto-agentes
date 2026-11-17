# Prueba del agente revisor

Borrador base: `ejemplos/guia_ejemplo.md`.

## Contradicción introducida

En la sección `## Explicación` del segundo borrador se agregó:

> El primer elemento de una lista siempre está en la posición 1.

Esto contradice el ejemplo de código (`nombres[0]` devuelve el primer elemento)
y el comportamiento real de Python, donde los índices empiezan en 0.

## Resultado 1: borrador coherente

# Guía de estudio: Listas de Python

## Explicación

Una lista conserva varios valores en un orden definido.

```python
nombres = ["Ana", "Luis"]
print(nombres[0])
```

## Práctica

Escribe una función que devuelva la cantidad de nombres de una lista.

## Revisión

- Se mantuvo la explicación original ya que define correctamente el concepto básico de lista.
- El código de ejemplo es claro, correcto y demuestra la indexación en listas sin errores.
- La consigna práctica es adecuada para ejercitar el concepto presentado y no requirió modificaciones.

---

## Resultado 2: borrador con contradicción

# Guía de estudio: Listas de Python

## Explicación

Una lista conserva varios valores en un orden definido. El primer elemento de una lista siempre está en la posición 0.

```python
nombres = ["Ana", "Luis"]
print(nombres[0])
```

## Práctica

Escribe una función que devuelva la cantidad de nombres de una lista.

## Revisión
- Se corrigió el error conceptual en la explicación: en Python las listas usan índices que comienzan en 0, no en 1.
- Se eliminó la contradicción existente entre el texto original (que indicaba posición 1) y el ejemplo en código (que accedía al índice `0`).
- La consigna de la sección Práctica se mantuvo sin cambios por ser adecuada y clara.
