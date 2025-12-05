from backend.controlador import (
    crear_jugador, hay_jugador, crear_mascota, alimentar_mascota, dormir_mascota,
    jugar_con_mascota, enviar_al_hospital, curar_en_hospital,
    ver_estado_mascota, preparar_liberacion, confirmar_liberacion,
    ver_mascotas_liberadas, salir_del_juego
)
from collections import deque
import json

# Historial de acciones
historial = deque(maxlen=5)

def guardar_estado(mascota):
    """
    Guarda el estado de una mascota en un archivo JSON.
    """
    datos = mascota.get_dict()
    with open("estado_mascota.json", "w") as f:
        json.dump(datos, f)

def cargar_estado():
    """
     Carga el estado de una mascota desde el archivo JSON `estado_mascota.json`.
    """
    try:
        with open("estado_mascota.json", "r") as f:
            datos = json.load(f)
            from mascota import Mascota
            return Mascota(datos["nombre"], datos["especie"])
    except FileNotFoundError:
        return None

def mostrar_historial():
    """
    Imprime por consola las últimas acciones registradas en el historial.
    """
    print("\nÚltimas acciones:")
    for accion in historial:
        print(f"- {accion}")

# Menú principal
def menu():
    print("\n--- PawPop 🐾 ---")
    print("1. Crear jugador")
    print("2. Crear mascota")
    print("3. Ver estado de mascota")
    print("4. Alimentar")
    print("5. Dormir")
    print("6. Jugar")
    print("7. Enviar al hospital")
    print("8. Curar en hospital")
    print("9. Preparar liberación")
    print("10. Confirmar liberación")
    print("11. Ver mascotas liberadas")
    print("12. Mostrar historial")
    print("13. Salir")

def main():
    print("Bienvenida a PawPop 🐾")

    while True:
        menu()
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            nombre = input("Nombre del jugador: ")
            mail = input("Mail del jugador: ")
            crear_jugador(nombre, mail)

        elif opcion == "2":
            if not hay_jugador():
                print("Primero debes crear un jugador.")
                continue # vuelve al menú sin pedir datos
            else:
                nombre = input("Nombre de la mascota: ")
                especie = input("Especie (Perro, Gato, Vaca, Conejo, Capibara): ")
                crear_mascota(nombre.capitalize(), especie.capitalize())
                historial.append(f"Se creó la mascota {nombre.capitalize()} ({especie.capitalize()})")
            """
            mascota_guardada = cargar_estado()
            if mascota_guardada:
                print(f"Se encontró una mascota guardada: {mascota_guardada.ver_nombre()} ({mascota_guardada.ver_especie()})")
                usar = input("¿Querés usar esta mascota? (s/n): ").lower()
                if usar == "s":
                    crear_mascota(mascota_guardada.ver_nombre(), mascota_guardada.ver_especie())
                    historial.append(f"Se cargó la mascota {mascota_guardada.ver_nombre()}")
                else:
                    nombre = input("Nombre de la nueva mascota: ")
                    especie = input("Especie (Perro, Gato, Vaca, Conejo, Capibara): ")
                    crear_mascota(nombre, especie)
                    historial.append(f"Se creó la mascota {nombre} ({especie})")
            """
        
        elif opcion == "3":
            ver_estado_mascota()

        elif opcion == "4":
            alimentar_mascota()
            historial.append("Mascota alimentada.")

        elif opcion == "5":
            dormir_mascota()
            historial.append("Mascota durmió.")

        elif opcion == "6":
            jugar_con_mascota()
            historial.append("Mascota jugó.")

        elif opcion == "7":
            enviar_al_hospital()
            historial.append("Mascota enviada al hospital.")

        elif opcion == "8":
            curar_en_hospital()
            historial.append("Mascota curada en el hospital.")

        elif opcion == "9":
            preparar_liberacion()
            historial.append("Mascota preparada para liberación.")

        elif opcion == "10":
            confirmar_liberacion()
            historial.append("Mascota liberada.")

        elif opcion == "11":
            ver_mascotas_liberadas()

        elif opcion == "12":
            mostrar_historial()

        elif opcion == "13":
            import os
            if os.path.exists("estado_mascota.json"):
                os.remove("estado_mascota.json")

            print("Estado borrado. ¡Hasta la próxima!")
            salir_del_juego()

        else:
            print("Opción inválida. Elegí del 1 al 13.")

if __name__ == "__main__":
    main()
    

