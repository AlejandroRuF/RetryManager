from pywinauto import Desktop, Application
import time
import re
import concurrent.futures  # Biblioteca para manejar hilos paralelos

ventana_objetivo = "optimizer"  # Reemplaza con el nombre o parte del título de la ventana objetivo
ventanas_procesadas = set()  # Conjunto para almacenar handles de las ventanas ya procesadas
boton_a_pulsar = "aceptar"
texto_dialog = ""


def bucle_detectar():
    """Detecta todas las ventanas activas con el nombre objetivo y lanza buscar_dialogos en un hilo separado si no está ya en proceso."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            try:
                ventanas_activas = Desktop(backend="uia").windows()  # Busca todas las ventanas activas
                for i, ventana in enumerate(ventanas_activas):
                    try:
                        titulo = ventana.window_text().strip()
                        handle = ventana.handle  # Identificador único de la ventana
                        if titulo:
                            print(f"{i + 1}. {titulo} (Handle: {handle})")

                            # Detectar si el título contiene la palabra objetivo y si el handle no ha sido procesado
                            if ventana_objetivo.lower() in titulo.lower() and handle not in ventanas_procesadas:
                                print(f"\nVentana detectada: {titulo} (Handle: {handle})\n")

                                # Agregar el handle al conjunto de ventanas procesadas
                                ventanas_procesadas.add(handle)

                                # Conectar a la ventana detectada
                                app = Application(backend="uia").connect(handle=handle)
                                ventana_encontrada = app.window(handle=handle)

                                # Ejecutar buscar_dialogos en un hilo separado
                                executor.submit(buscar_dialogos, ventana_encontrada, handle)

                    except Exception as e:
                        print(f"{i + 1}. Error al procesar la ventana '{ventana.window_text()}': {e}")

            except Exception as e:
                print(f"Error general detectando ventana: {e}")

            time.sleep(1)  # Pausa de 1 segundo para evitar uso excesivo de recursos


def buscar_dialogos(ventana, handle):
    """Busca cuadros de diálogo dentro de la ventana detectada y lista sus botones."""
    try:
        cuadros_dialogo = ventana.descendants(control_type="Window")  # Busca ventanas hijas (cuadros de diálogo)
        if cuadros_dialogo:
            print(f"Cuadros de diálogo encontrados en la ventana '{ventana.window_text()}':")
            for i, dialogo in enumerate(cuadros_dialogo):
                try:
                    titulo_dialogo = dialogo.window_text().strip()
                    if titulo_dialogo:
                        print(f"\n  {i + 1}. Cuadro de diálogo: {titulo_dialogo}")
                        print("  -----------------------------")
                        lista_botones(dialogo)  # Llamada directa para listar botones
                        print("  -----------------------------\n")
                except Exception as e:
                    print(f"  Error al procesar el cuadro de diálogo '{dialogo.window_text()}': {e}")
        else:
            print("No se encontraron cuadros de diálogo en esta ventana.")
    except Exception as e:
        print(f"Error al buscar cuadros de diálogo -> {e}")
    finally:
        # Eliminar el handle del conjunto después de procesar la ventana
        if handle in ventanas_procesadas:
            ventanas_procesadas.remove(handle)
            print(f"Handle {handle} eliminado de ventanas procesadas.")


def lista_botones(ventana):
    """Lista todos los botones disponibles en el cuadro de diálogo detectado."""
    try:
        botones = ventana.descendants(control_type="Button")  # Busca todos los botones dentro del cuadro de diálogo
        if botones:
            print("  Botones detectados:")
            for i, boton in enumerate(botones):
                boton_texto = boton.window_text()
                print(f"    {i + 1}. {boton.window_text()} (Control ID: {boton.control_id()})")

                if boton_texto.lower() == boton_a_pulsar.lower():
                    pulsar_boton(boton)

        else:
            print("  No se encontraron botones en el cuadro de diálogo.")
    except Exception as e:
        print(f"  Error al listar los botones -> {e}")


def pulsar_boton(boton):
    """Pulsar el botón identificado por su texto."""
    try:
        boton.click()
        print(f"  Botón '{boton.window_text()}' pulsado correctamente.")
    except Exception as e:
        print(f"  Error al pulsar el botón '{boton.window_text()}': {e}")

if __name__ == "__main__":
    print("Esperando la aparición de las ventanas objetivo...\n")
    bucle_detectar()
