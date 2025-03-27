# RetryManager

RetryManager es una herramienta sencilla pensada para automatizar la interacción con ventanas del sistema en Windows. Permite buscar ventanas activas por su nombre y simular la pulsación de botones específicos dentro de ellas, como por ejemplo "aceptar".

## ¿Para qué sirve?

- Detecta ventanas activas en el sistema.
- Busca por coincidencias en el título de la ventana.
- Intenta hacer clic automáticamente en un botón dentro de esa ventana (por defecto, el botón "aceptar").
- Se ejecuta en bucle y puede gestionar varias ventanas si aparecen repetidamente.

Es útil para automatizar diálogos repetitivos de aplicaciones o scripts en Windows.

## Requisitos

- Sistema operativo Windows.
- Python 3.7 o superior.
- Dependencias instaladas (especialmente `pywinauto`).

## Instalación

1. Descarga el proyecto y descomprime el archivo `.zip`.
2. Abre una terminal en la carpeta `RetryManager`.
3. (Opcional) Activa el entorno virtual incluido:

```bash
.\.venv\Scriptsctivate
```

4. Si prefieres usar tu propio entorno, instala manualmente la dependencia:

```bash
pip install pywinauto
```

## Uso

Ejecuta el archivo principal con:

```bash
python RetryWindows.py
```

El programa pedirá que introduzcas el nombre (o parte del nombre) de la ventana a buscar. Luego intentará encontrarla y hacer clic en el botón "aceptar" dentro de ella.

> Puedes modificar el botón que se desea pulsar y otros filtros editando directamente el código en `RetryWindows.py`.

## Archivos principales

- `RetryWindows.py`: Script principal de detección y acción sobre ventanas.
- `RetryWindowsFeedback.py`: Versión alternativa o extendida del script base (puede incluir funcionalidades adicionales).
