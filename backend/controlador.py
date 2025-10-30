from backend.jugador import Jugador
from backend.espacio import Campo, Hospital, Libertad

# Instancias globales
campo = Campo()
hospital = Hospital()
libertad = Libertad()
jugador = None 


def crear_jugador(nombre, mail):
    global jugador
    try:
        jugador = Jugador(nombre, mail, campo)
        print(f"Jugador {nombre} creado con éxito.")
    except ValueError as e:
        print(str(e))

def hay_jugador():
    return jugador is not None

def crear_mascota(nombre, especie):
    especies_validas = ["perro", "gato", "vaca", "conejo", "capibara"]

    if not jugador:
        print("Primero debes crear un jugador.")
        return

    if especie.lower() not in especies_validas:
        print(f"Especie inválida. Elegí entre: {', '.join(especies_validas)}")
        return

    campo.agregar(nombre, especie)
    print(f"Mascota {nombre} ({especie}) creada con éxito.")

def alimentar_mascota():
    if campo.mascota:
        campo.alimentar()
    else:
        print("No hay mascota en el campo.")

def dormir_mascota():
    if campo.mascota:
        campo.mascota.dormir()
    else:
        print("No hay mascota en el campo.")
    
def jugar_con_mascota():
    if campo.mascota:
        campo.mascota.jugar()
    else:
        print("No hay mascota en el campo.")
        
def enviar_al_hospital():
    if campo.mascota:
        campo.curar_mascota(hospital)
    else:
        print("No hay mascota para enviar al hospital.")

def curar_en_hospital():
    if hospital.mascota:
        hospital.curar_mascota()
    else:
        print("No hay mascota en el hospital.")

def ver_estado_mascota():
    if campo.mascota:
        campo.ver()
    else:
        print("No hay mascota en el campo.")
    
def preparar_liberacion():
    if campo.mascota:
        hospital.eliminar(libertad)
    else:
        print("No hay mascota para liberar.")

def confirmar_liberacion():
    if libertad.mascota:
        libertad.alimentar(libertad.mascota)
        jugador.mascotas_liberadas.append(hospital.mascota.get_dict())
        hospital.mascota = None
        campo.mascota = None
        libertad.mascota = None
        print("Mascota liberada. Podés crear una nueva.")
    else:
        print("No hay mascota lista para liberar.")

def ver_mascotas_liberadas():
    if jugador:
        libertad.ver()
    else:
        print("No hay jugador creado.")

def salir_del_juego():
    if jugador:
        libertad.eliminar(jugador)
    else:
        print("No hay jugador creado.")