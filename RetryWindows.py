from pywinauto import Desktop, Application
import time
import re
import concurrent.futures

# ventana_objetivo = ""  # Reemplaza con el nombre o parte del título de la ventana objetivo
ventana_objetivo = input("Introduce el objetivo de la ventana: ")
ventanas_procesadas = set()  # Guarda las ID de las ventanas Procesadas
boton_a_pulsar = "aceptar" # Texto del boton a pulsar
texto_dialog = "" # Texto descriptivo dentro del dialog para habilitar la opcion de filtrar por este
title_dialog = "" # Titulo del dialogo para habilitar el filtrado por este


def bucle_detectar():

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            try:

                ventanas_activas = Desktop(backend="uia").windows()
                for i, ventana in enumerate(ventanas_activas):
                    try:

                        titulo = ventana.window_text().strip()
                        id_ventana = ventana.handle

                        if titulo:
                            # Detectar si el título contiene la palabra objetivo y si el ID no ha sido procesado
                            if ventana_objetivo.lower() in titulo.lower().split(" ") and id_ventana not in ventanas_procesadas:
                                ventanas_procesadas.add(id_ventana)
                                # Conectar a la ventana detectada
                                app = Application(backend="uia").connect(handle=id_ventana)
                                ventana_encontrada = app.window(handle=id_ventana)
                                # Busca si la ventana tiene dialogos
                                executor.submit(buscar_dialogos, ventana_encontrada, id_ventana)

                    except Exception as e:
                        print(f"{i + 1}. Error en ventana {ventana.window_text()}-> {e}")

            except Exception as e:
                print(f"Error detectando ventana -> {e}")

            time.sleep(1)


def buscar_dialogos(ventana, id):
    try:

        cuadros_dialogo = ventana.descendants(control_type="Window") #Busca si tiene ventanas Child

        if cuadros_dialogo:

            for i, dialogo in enumerate(cuadros_dialogo):
                try:
                    titulo_dialogo = dialogo.window_text().strip()


                    # Para filtrar por el titulo del child
                    # if title_dialog in titulo_dialogo.split(" "):

                    # Para filtrar por contenido de la ventana
                    # mensaje_dialogo = obtener_contenido_mensaje(dialogo)
                    # if mensaje_dialogo and filtro_contenido(titulo_dialogo, mensaje_dialogo):

                    lista_botones(dialogo)

                except Exception as e:
                    print(f"  Error en dialogo {dialogo.window_text()} -> {e}")

    except Exception as e:
        print(f"Error al buscar cuadros de diálogo -> {e}")

    finally:
        # Eliminar el ID del conjunto después de procesar la ventana
        if id in ventanas_procesadas:
            ventanas_procesadas.remove(id)


def lista_botones(ventana):
    try:
        botones = ventana.descendants(control_type="Button")  # Busca todos los botones dentro del cuadro de diálogo
        if botones:
            for i, boton in enumerate(botones):
                boton_texto = boton.window_text()

                if boton_texto.lower() == boton_a_pulsar.lower():
                    pulsar_boton(boton)

    except Exception as e:
        print(f"  Error al listar los botones -> {e}")


def pulsar_boton(boton):
    try:
        boton.click()
    except Exception as e:
        print(f"  Error al pulsar el botón {boton.window_text()} -> {e}")


def obtener_contenido_mensaje(dialogo):
    try:
        controles_texto = dialogo.descendants(control_type="Text")  # Busca todos los controles de tipo 'Text'

        for control in controles_texto:
            texto = control.window_text().strip()
            if texto:
                return texto
        return None
    except Exception as e:
        print(f"  Error al obtener el contenido del mensaje: {e}")
        return None


def filtro_contenido(texto_clave, mensaje):
    try:
        # Expresión regular
        patron = rf"\b{re.escape(texto_clave)}\b"
        if re.search(patron, mensaje, re.IGNORECASE):
            return True
        return False
    except Exception as e:
        print(f"Error al buscar coincidencia -> {e}")
        return False

if __name__ == "__main__":
    bucle_detectar()
