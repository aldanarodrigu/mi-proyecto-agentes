# Guía de estudio: funciones

## Explicación

Una **función** es un bloque de código reutilizable que realiza una tarea específica. Sirve para organizar el código, evitar repetir instrucciones y hacer que tu programa sea más fácil de leer. Se define usando la palabra clave `def`, se le puede pasar información (parámetros) y puede devolver un resultado (con `return`).

```python
# Definimos la función
def saludar(nombre):
    mensaje = f"¡Hola, {nombre}!"
    return mensaje


# Llamamos a la función
resultado = saludar("Ana")
print(resultado)  # Imprime: ¡Hola, Ana!
```

### Error frecuente
Confundir **`print()`** con **`return`**. 
* Usa `print()` cuando solo quieras mostrar algo en la pantalla.
* Usa `return` si necesitas que la función le devuelva un valor al programa para guardar en una variable o usarlo en otro cálculo. Si no pones `return`, la función devolverá `None` por defecto.

## Práctica

**1. Ejercicio**  
Crea una función llamada `multiplicar_por_tres` que reciba un número como parámetro y devuelva el resultado de multiplicar ese número por 3. Luego, llama a la función pasándole el número `5`, guarda el valor devuelto en una variable y muestra el resultado en la pantalla usando `print()`.

---

**2. Criterios de aceptación**  
1. La función debe estar definida con la palabra clave `def` y aceptar exactamente un parámetro.  
2. La función debe calcular la multiplicación y utilizar `return` para devolver el valor (no debe usar `print()` dentro de la función).  
3. El programa debe llamar a la función pasándole un argumento, guardar el retorno en una variable y mostrar esa variable en la terminal.

---

**3. Pista**  
Recuerda que dentro de la función puedes usar el operador `*` para multiplicar el parámetro por 3. Para devolver ese valor hacia afuera de la función para que puedas guardarlo en una variable, asegúrate de colocar la palabra clave `return` antes del cálculo o del resultado.

## Revisión
- El contenido conceptual y los ejemplos de código proporcionados eran correctos y claros, por lo que no requirieron modificaciones de fondo.
- Se eliminaron saludos y subencabezados redundantes para mantener una estructura más limpia y profesional dentro de las secciones requeridas.
- La sección de práctica describe adecuadamente el ejercicio y los criterios de evaluación.