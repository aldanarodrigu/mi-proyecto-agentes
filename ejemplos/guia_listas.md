# Guía de estudio: listas

## Explicación

Una **lista** es una estructura que te permite guardar varios valores (números, texto, otros objetos) en una sola variable, manteniendo un orden determinado. Son mutables, lo que significa que podés modificar, agregar o quitar elementos después de haberlas creado. Se definen utilizando corchetes `[]`.

---

### Ejemplo

```python
# Creando una lista de frutas
frutas = ["manzana", "banana", "naranja"]

# Accediendo al primer elemento (índice 0)
print(frutas[0])  # Muestra: manzana

# Agregando un nuevo elemento
frutas.append("pera")
print(frutas)  # Muestra: ['manzana', 'banana', 'naranja', 'pera']
```

---

### Error frecuente
El error más común de los principiantes es **olvidar que en Python los índices empiezan en 0, no en 1**. 

Si tenés una lista de 3 elementos, sus posiciones son `0`, `1` y `2`. Si intentás acceder a la posición `3` (`frutas[3]`), Python te dará un error del tipo `IndexError: list index out of range` (índice fuera de rango).

## Práctica

### 1. Ejercicio

Crea un programa en Python que defina una lista con los nombres de tres colores. A continuación:
1. Imprime en pantalla únicamente el primer color de la lista.
2. Agrega un cuarto color al final de la lista.
3. Imprime la lista completa para verificar que el nuevo color se añadió correctamente.

---

### 2. Criterios de aceptación

1. La lista inicial debe crearse usando corchetes `[]` y contener exactamente tres elementos de tipo texto.
2. El acceso al primer elemento para imprimirlo debe hacerse mediante el índice `0`.
3. Se debe utilizar el método `.append()` para agregar el cuarto elemento antes de mostrar la lista final.

---

### 3. Pista

Recordá que los índices en Python empiezan a contar desde el `0`, por lo que el primer elemento se consulta con `nombre_de_lista[0]`. Para agregar un elemento nuevo, podés llamar a `.append("tu_color")` usando la misma variable donde guardaste la lista.

## Revisión
- Se mantuvo la totalidad de la estructura original, los conceptos teóricos y los ejemplos de código por ser correctos y adecuados para el nivel.
- Se removió la frase de saludo inicial en la explicación para dar paso directo al contenido didáctico.
- No hicieron falta correcciones conceptuales ni sintácticas en la sección de práctica ni en la explicación del error frecuente.