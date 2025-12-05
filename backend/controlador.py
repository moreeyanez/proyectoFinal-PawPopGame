from backend.jugador import Jugador
from backend.espacio import Campo, Hospital, Libertad

# Instancias globales
campo = Campo()
hospital = Hospital()
libertad = Libertad()
jugador = None

# ---------------------
# Helpers seguros de estado/energía
# ---------------------
def _leer_energia_seguro(mascota):
    """
    Obtiene de forma segura el nivel de energía de una mascota.
    """
    try:
        if hasattr(mascota, "ver_energia") and callable(mascota.ver_energia):
            return mascota.ver_energia()
    except Exception:
        pass
    for nombre in ("energia", "_energia", "nivel_energia"):
        if hasattr(mascota, nombre):
            return getattr(mascota, nombre)
    return 0

def _set_energia_seguro(mascota, valor):
    """
    Establece de forma segura el nivel de energía de una mascota.
    """
    # Busca APIs públicas primero
    if hasattr(mascota, "set_energia") and callable(mascota.set_energia):
        mascota.set_energia(valor)
        return True
    if hasattr(mascota, "ajustar_energia") and callable(mascota.ajustar_energia):
        actual = _leer_energia_seguro(mascota)
        delta = int(valor) - int(actual)
        mascota.ajustar_energia(delta)
        return True
    # Fallback a atributos comunes
    for nombre in ("energia", "_energia", "nivel_energia"):
        if hasattr(mascota, nombre):
            setattr(mascota, nombre, int(max(0, min(100, valor))))
            return True
    return False

def _apagar_enfermedad_seguro(mascota):
    """
    Desactiva de forma segura cualquier indicador de enfermedad en un objeto mascota.
    """
    # Apaga cualquier flag típico de "enfermo"
    for nombre in ("enfermo", "esta_enfermo", "estado_enfermo"):
        if hasattr(mascota, nombre):
            setattr(mascota, nombre, False)
            return True
    return False

# ---------------------
# Jugador y creación
# ---------------------
def crear_jugador(nombre, mail):
    """
    Crea una instancia global de Jugador y la asigna a la variable `jugador`.
    """
    global jugador
    try:
        jugador = Jugador(nombre, mail, campo)
        print(f"Jugador {nombre} creado con éxito.")
    except ValueError as e:
        print(str(e))

def hay_jugador():
    """
    Indica si ya existe un jugador creado en la sesión.
    """
    return jugador is not None

def crear_mascota(nombre, especie):
    """
    Crea una mascota en el campo del jugador actual.
    """
    especies_validas = ["perro", "gato", "vaca", "conejo", "capibara"]

    if not jugador:
        print("Primero debes crear un jugador.")
        return

    if especie.lower() not in especies_validas:
        print(f"Especie inválida. Elegí entre: {', '.join(especies_validas)}")
        return

    campo.agregar(nombre, especie)
    print(f"Mascota {nombre} ({especie}) creada con éxito.")

# ---------------------
# Acciones en Campo
# ---------------------
def alimentar_mascota():
    """
    Alimenta la mascota que está actualmente en el campo.
    """
    if campo.mascota:
        campo.alimentar()
    else:
        print("No hay mascota en el campo.")

def dormir_mascota():
    """
    Hace que la mascota del campo duerma y recupere energía.
    """
    if campo.mascota:
        campo.mascota.dormir()
    else:
        print("No hay mascota en el campo.")

def jugar_con_mascota():
    """
    Inicia la acción de juego con la mascota que está en el campo.
    """
    if campo.mascota:
        campo.mascota.jugar()
    else:
        print("No hay mascota en el campo.")

# ---------------------
# Flujo Hospital
# ---------------------
def enviar_al_hospital():
    """
    Mueve la mascota del campo al hospital usando la API de espacios.
    No reinicia el juego ni crea una nueva mascota.
    """
    global hospital, campo
    if campo.mascota:
        campo.curar_mascota(hospital)  # según tu diseño, esto transfiere la mascota al hospital
        print("[backend] Mascota enviada al hospital.")
    else:
        print("No hay mascota para enviar al hospital.")

def curar_en_hospital():
    """
    Cura la mascota que está en el hospital:
    - Apaga el flag de enfermedad
    - Sube energía +30 (cap 100)
    Devuelve dict con estado, para que el frontend confirme y muestre cambios.
    """
    if not hospital.mascota:
        print("[backend] No hay mascota en hospital para curar.")
        return {"ok": False, "msg": "No hay mascota en hospital"}

    m = hospital.mascota
    m.curar()  # 🔧 Esto restaura energía=80 y alimentación=80 y apaga enfermo

    estado = m.obtener_estado_visual() if hasattr(m, "obtener_estado_visual") else "feliz"
    print(f"[backend] Mascota curada en hospital: energía=80, alimentación=80, estado={estado}")
    return {"ok": True, "energia": 80, "alimentacion": 80, "estado": estado}

# ---------------------
# Estado y liberación
# ---------------------
def ver_estado_mascota():
    """
    Muestra por consola el estado de la mascota que está en el campo.
    """
    if campo.mascota:
        campo.ver()
    else:
        print("No hay mascota en el campo.")

def preparar_liberacion():
    """
    Prepara la liberación de la mascota que se encuentra en el hospital.
    """
    if hospital.mascota:
        hospital.eliminar(libertad)  # según tu diseño, transfiere mascota al espacio Libertad
        print("[backend] Mascota preparada para liberación.")
    else:
        print("No hay mascota para liberar en hospital.")

def confirmar_liberacion():
    """
    Confirma y finaliza la liberación de la mascota que está en Libertad.
    """
    if libertad.mascota:
        # Guardar en historial del jugador
        jugador.mascotas_liberadas.append(libertad.mascota.get_dict())

        # Mensaje de éxito
        print(f"{libertad.mascota.ver_nombre()} ha sido liberada. Podés crear una nueva.")

        # Limpiar referencias en todos los espacios
        libertad.mascota = None
        campo.mascota = None
        hospital.mascota = None
    else:
        print("No hay mascota lista para liberar.")

def ver_mascotas_liberadas():
    """
    Muestra por consola la lista de mascotas liberadas (registro en Libertad).
    """
    if jugador:
        libertad.ver()
    else:
        print("No hay jugador creado.")

def obtener_mascotas_liberadas():
    """
    Devuelve la lista de mascotas liberadas del jugador actual.
    """
    if jugador:
        return jugador.mascotas_liberadas
    return []

def salir_del_juego():
    """
    Finaliza la sesión del juego.
    """
    if jugador:
        libertad.eliminar(jugador)
    else:
        print("No hay jugador creado.")
    print("Juego finalizado. ¡Gracias por jugar!")