# Agentes de IA con Python

Aplicación de consola que genera una guía de estudio en Markdown sobre un tema
de Python indicado por la persona usuaria. Tres agentes construidos con ADK y
Gemini colaboran en secuencia:

1. **Explicador** (`agentes/explicador.py`): explica el tema con un ejemplo breve.
2. **Diseñador de práctica** (`agentes/disenador_practica.py`): propone un ejercicio corto.
3. **Revisor** (`agentes/revisor.py`): comprueba la coherencia y entrega la guía final.

`main.py` coordina el flujo, y `herramientas/` valida el resultado y lo guarda
de forma segura en `salida/`. Un modo simulado permite probar todo sin consumir
API. En `ejemplos/` hay dos guías generadas con Gemini:
[`guia_listas.md`](ejemplos/guia_listas.md) y
[`guia_funciones.md`](ejemplos/guia_funciones.md).

La imagen creó estos archivos con `iniciar-proyecto`. La
[guía de trabajo con Docker y VS Code](docs/trabajar-con-docker.md) explica el
flujo de trabajo y la conexión opcional de VS Code al contenedor.

## Antes de comenzar

La imagen Docker proporcionada contiene Python, ADK y las dependencias necesarias.

Configura la imagen pública preparada para este proyecto una vez en cada
terminal y descárgala:

```bash
export AGENTS_IMAGE="ghcr.io/hbtn-edu/ai-agents-python:0.4.0"
docker pull "$AGENTS_IMAGE"
```

Ubícate en la carpeta local creada al inicializar el proyecto. `"$PWD"` comparte la carpeta
actual con el contenedor para que puedas editarla con tus herramientas habituales.

```bash
# Comprobar Python, ADK y el entorno sin consumir API
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --sin-api

# Ejecutar las pruebas básicas del starter pack
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" \
  python -m pytest -q pruebas/test_entorno.py pruebas/test_runtime.py

# Ejecutar todas las pruebas públicas de las tareas obligatorias durante el proyecto
docker run --rm -it --user "$(id -u):$(id -g)" -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m pytest -q -k 'not extension'

# Ejecutar la aplicación después de configurar .env
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python main.py
```

La prueba de la extensión opcional se ejecuta con `python -m pytest -q pruebas/test_flujo.py`,
usando el mismo comando Docker y sin el filtro `-k`.

Las pruebas de agentes, archivos, validación y flujo fallan al comienzo porque
corresponden al trabajo que debes completar. Las pruebas de entorno y runtime
deben pasar desde el primer momento.

### Opción: VS Code dentro del contenedor

Abre la carpeta en VS Code con la extensión **Dev Containers** y selecciona
**Dev Containers: Reopen in Container**. En la terminal conectada de VS Code
se ejecutan directamente los comandos Python, sin el prefijo `docker run ...`:

```bash
python -m runtime.diagnostico --sin-api
python -m pytest -q pruebas/test_entorno.py pruebas/test_runtime.py
```

Los comandos Git se siguen ejecutando en la terminal local. Si cambias `.env`,
consulta en la [guía](docs/trabajar-con-docker.md#vs-code-dentro-del-contenedor-opcional)
cómo recargar la configuración del contenedor.

## Configuración segura de Gemini

1. Abre [Google AI Studio](https://aistudio.google.com/apikey) e inicia sesión.
2. Crea una clave en la sección de claves de API. Si la cuenta requiere asociar
   un proyecto de Google Cloud, sigue la
   [guía de creación y gestión de claves](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419).
3. Edita el `.env` creado al inicializar y completa `GOOGLE_API_KEY` con la clave.
4. Conserva `GEMINI_MODEL=gemini-3.5-flash` y las demás variables del archivo.
5. Comprueba con `git check-ignore .env` que Git ignora el archivo.

```bash
git check-ignore .env

docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --sin-api
```

La siguiente comprobación realiza una llamada real y consume cuota. Ejecútala
una vez para verificar el acceso:

```bash
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
  "$AGENTS_IMAGE" python -m runtime.diagnostico --con-api
```

El diagnóstico informa si la clave está configurada, pero nunca muestra su
valor ni una parte de ella.

### Si el servicio no está disponible

El modelo configurado es `gemini-3.5-flash`, probado con este starter pack.
Si aparece `503 UNAVAILABLE` o «El servicio no está disponible», termina esa
ejecución, espera al menos un minuto y vuelve a ejecutar manualmente el mismo
comando una sola vez. Si vuelve a fallar, registra el modelo, la hora y el
mensaje, y consulta el [estado del servicio](https://aistudio.google.com/status).
Mientras se restablece, el modo simulado permite comprobar las operaciones locales.

Ante un error de cuota (`429`), detén las llamadas y revisa los límites de la
cuenta antes de una nueva ejecución. Consulta la
[guía de solución de problemas](https://ai.google.dev/gemini-api/docs/troubleshooting?hl=es-419),
solamente «Estrategia de reintentos» y «Verifica si tienes el modelo correcto».

## Modo simulado

Las respuestas fijas incluidas permiten comprobar el flujo sin consumir API.
La calidad de las respuestas a temas diferentes se verifica con ejecuciones reales.

```bash
docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -e MODO_SIMULADO=1 \
  -v "$PWD:/workspace" -w /workspace "$AGENTS_IMAGE" python main.py
```

## Ejemplo de ejecución

```text
$ docker run --rm -it --user "$(id -u):$(id -g)" --env-file .env -v "$PWD:/workspace" -w /workspace \
    "$AGENTS_IMAGE" python main.py
Tema de Python: funciones
Guía guardada en: salida/guia-funciones.md
```

Antes del mensaje final pueden aparecer advertencias del SDK (por ejemplo,
sobre *automatic function calling*); no indican un fallo. La guía se guarda en
`salida/` con un nombre derivado del tema, sin tildes ni símbolos.

## Flujo

```text
tema → explicador → diseñador → borrador → revisor
     → guía final → validación → archivo Markdown
```

`ejecutar_flujo(tema, ejecutar=ejecutar_agente, permitir_correccion=False)` en
`main.py` invoca una vez a cada agente. El diseñador recibe la explicación
completa; el borrador (`# Guía de estudio: <tema>`, `## Explicación`,
`## Práctica`) se entrega completo al revisor, cuya respuesta es la guía final.
La guía se valida antes de guardarse:

- Si es válida, se guarda y se devuelve `{"ok": True, "ruta": ...}`.
- Si no lo es, no se guarda nada y se devuelve `{"ok": False, "faltantes": [...]}`.
- Con `permitir_correccion=True`, una guía inválida se envía al revisor una
  única vez más junto con la lista de faltantes.

## Agentes

| Agente | Archivo | Entrada | Responsabilidad |
| --- | --- | --- | --- |
| `explicador_python` | `agentes/explicador.py` | Tema | Explicación breve, ejemplo de código y error frecuente. |
| `disenador_practica` | `agentes/disenador_practica.py` | Tema y explicación | Ejercicio, tres criterios de aceptación verificables y una pista, sin solución. |
| `revisor_python` | `agentes/revisor.py` | Borrador completo | Corrige solo lo necesario y agrega `## Revisión`. |

Los tres usan el modelo indicado en `GEMINI_MODEL`.

## Herramientas

- `herramientas/validacion.py` – `validar_guia(contenido)`: comprueba el título
  `# Guía de estudio:`, las secciones `## Explicación`, `## Práctica` y
  `## Revisión`, un bloque ```` ```python ```` y la ausencia de la clave de API.
  Devuelve `{"valida": bool, "faltantes": [...]}`.
- `herramientas/archivos.py` – `guardar_markdown(nombre, contenido)`: acepta
  solo nombres `.md` sin rutas, escribe dentro de `salida/` mediante un archivo
  temporal y lo reemplaza al terminar; si la escritura falla, borra el temporal
  y no deja contenido parcial.

## Configuración

Variables de `.env` (nunca se versiona):

| Variable | Uso |
| --- | --- |
| `GOOGLE_API_KEY` | Clave de Gemini. Obligatoria para ejecuciones reales. |
| `GEMINI_MODEL` | Modelo utilizado por los agentes (`gemini-3.5-flash`). |
| `LLM_PROVIDER` | Proveedor; solo se admite `gemini`. |
| `GOOGLE_GENAI_USE_VERTEXAI` | Mantener el valor del archivo creado al iniciar. |
| `MODO_SIMULADO` | Con `1`, usa respuestas fijas y no llama a la API. |

## Errores frecuentes

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| `Error: El tema no puede estar vacío.` | Se pulsó Enter sin escribir un tema. | Escribir un tema. |
| `Error de configuración: Falta configurar: ...` | `.env` incompleto o no pasado con `--env-file`. | Completar `.env` y repetir. |
| `Límite de uso: ...` (429) | Cuota o frecuencia agotada. | Detener las llamadas y revisar los límites de la cuenta. |
| `Servicio no disponible: ...` (503) | Alta demanda o problema de red. | Esperar al menos un minuto y reintentar una sola vez (ver más arriba). |
| `Respuesta vacía: ...` | El agente terminó sin texto. | Repetir más tarde o probar en modo simulado. |
| `La guía no es válida y no se guardó. Faltan: ...` | La guía del revisor no cumple la estructura. | Repetir o usar `permitir_correccion=True`. |
| `Error al guardar: ...` | Sin permisos o sin espacio en `salida/`. | Revisar permisos (`--user "$(id -u):$(id -g)"`). |

Ante un error de cuota o de red el programa termina sin volver a invocar al
ejecutor. Ninguno de estos mensajes muestra la clave ni fragmentos de ella.

## Estructura

- `main.py`: flujo secuencial y mensajes finales.
- `agentes/`: definición de cada agente.
- `herramientas/`: guardado seguro y validación determinista.
- `runtime/`: infraestructura de ejecución suministrada.
- `pruebas/`: pruebas que no consumen API (incluye `test_errores.py`).
- `ejemplos/`: respuestas simuladas y guías generadas con Gemini.
- `salida/`: archivos generados, ignorados por Git.

## Privacidad y seguridad

- Utiliza datos ficticios y limita el contexto enviado a la información necesaria.
- Mantén la clave en `.env`, excluida de Git, documentación, capturas y mensajes.
- Si una clave se expone, revócala y reemplázala.
- Las guías de `ejemplos/` se revisaron para que no contengan datos personales;
  los nombres que aparecen en el código son ficticios.
- `validar_guia` rechaza cualquier guía que contenga la clave configurada, de
  modo que no llega a guardarse.

## Limitaciones

- Solo se admite Gemini (`LLM_PROVIDER=gemini`); otro proveedor requiere
  adaptar `runtime/ejecutor.py`.
- La validación es estructural: confirma que existan las secciones y un bloque
  de código, pero no que la explicación sea correcta ni que el código funcione.
- El contenido varía entre ejecuciones y puede contener errores; la revisión
  humana sigue siendo necesaria.
- Cada guía requiere tres llamadas al modelo (cuatro con corrección), lo que
  consume cuota y depende de la disponibilidad del servicio.
- Las respuestas simuladas son fijas y no reflejan el tema escrito.
- Ejecutar dos veces el mismo tema reemplaza el archivo anterior en `salida/`.

## Reflexión

**¿Qué diferencia hay entre una llamada directa a un modelo y un agente?**
Una llamada directa envía un texto y recibe otro, sin más estructura. Un agente
agrupa el modelo con un nombre, una descripción y unas instrucciones
permanentes que definen su rol, y se ejecuta mediante un *runner* que gestiona
la sesión y los eventos. Así cada agente cumple un papel estable y puede
combinarse con otros o con herramientas.

**¿Qué responsabilidad tiene cada agente y cada herramienta?**
El explicador presenta el concepto con un ejemplo y un error frecuente; el
diseñador propone una práctica verificable a partir de esa explicación; el
revisor corrige el borrador y deja constancia en `## Revisión`.
`validar_guia` decide si la guía cumple los requisitos y `guardar_markdown` la
escribe de forma segura en `salida/`. `main.py` solo coordina el orden.

**¿Qué parte es determinista y cuál puede variar?**
Es determinista el orden del flujo, la construcción del borrador, la
validación, el nombre del archivo, el guardado y los mensajes de error. Varía
el texto producido por los agentes: con el mismo tema, dos ejecuciones pueden
dar explicaciones, ejercicios y revisiones distintas, o incluso una guía que
no cumpla la estructura.

**¿Por qué se valida con Python además de usar un revisor?**
El revisor también es un modelo: puede omitir una sección, cambiar el título o
añadir texto fuera de la guía. La validación en Python es rápida, gratuita,
reproducible y comprobable con pruebas, por lo que garantiza que nunca se
guarde una guía incompleta o con la clave, cosa que el revisor no puede
garantizar.

**¿Qué cambiaría al utilizar otro proveedor o un modelo local?**
Cambiarían la configuración (variables, credenciales o la URL del servidor
local), el valor del modelo de cada agente y la parte de `runtime/ejecutor.py`
que valida el proveedor y clasifica sus errores (códigos de cuota, red o
disponibilidad propios). Con un modelo local desaparecen la cuota y el envío
de datos a terceros, pero dependen del equipo la velocidad y la calidad, y
puede hacer falta ajustar las instrucciones. El flujo, la validación, el
guardado y las pruebas con ejecutores falsos no cambiarían.
