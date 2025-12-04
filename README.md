🐾 PawPop – Proyecto Final - Matu, Muñoz, Yañez, Pirez y Valle

-------------------------------------------------------------------
📌 Descripción General
-------------------------------------------------------------------
PawPop es un videojuego desarrollado en Python + Pygame, donde el jugador cuida una mascota virtual que puede comer,
dormir, jugar, enfermarse, curarse en un hospital y hasta ser liberada al campo.

El proyecto está dividido claramente en dos capas:
- backend/ → Lógica del juego, reglas internas, estado de la mascota, hospital, campo, liberación, etc.
- frontend/ → Pantallas visuales programadas con Pygame que interactúan con el backend.

Además, se incluye un sistema de persistencia mediante JSON, y un flujo de pantallas bien definido.

-------------------------------------------------------------------
🎮 Flujo General del Juego
-------------------------------------------------------------------
Pantalla de Inicio
Pantalla del Huevo (creación del jugador)
Pantalla de Nombrar Mascota
Pantalla de Casa
    - alimentar
    - jugar
    - dormir
    - curar
Si se enferma → Pantalla Hospital
Mascota sana → volver a la casa
Si el jugador decide → Pantalla Liberación
Liberación → Se guarda en historial
Pantalla Historial (lista de mascotas liberadas)

-------------------------------------------------------------------
🧠 Backend — Lógica del Juego
-------------------------------------------------------------------
mascota.py
- Clase Mascota
- Atributos: nombre, especie, alimentación, energía, estado_visual, estado, historial_acciones.
- Métodos clave:
    ver_nombre, ver_especie, ver_energia…
    comer(), jugar(), dormir()
    enfermar(), curar(), empachar()
    actualizar_estado_visual()

Es el núcleo del estado del juego.

controlador.py
Maneja la interacción entre pantallas y reglas:
    ✔️ crear_jugador
    ✔️ crear_mascota
    ✔️ obtener_mascotas_liberadas
    ✔️ preparar_liberacion
    ✔️ enviar_al_hospital
También mantiene el objeto: "campo.mascota" que se usa en todo el juego.

hospital.py
    - Cura a la mascota después de un tiempo.
    - Lleva registro de ingreso y salida.
    -  Función principal: curar_en_hospital().

campo.py 
    - Representa el campo donde la mascota queda cuando es liberada.
    - Contiene métodos para almacenar y obtener la lista de mascotas liberadas.

liberacion.py
    - Envía la mascota al campo
    - Guarda su info en un historial persistente
    - Resetea el campo para una nueva mascota

data.JSON
Archivo donde se guarda
    - mascota actual 
    - historial de liberación
    - estado del hospital

-------------------------------------------------------------------
🖼️ Frontend — Pantallas con Pygame
-------------------------------------------------------------------
Cada pantalla está completamente desacoplada y organizada.

pantallaInicio.py
    - Muestra el menú inicial
    - Botón "Iniciar"
    - Pasa a pantallaHuevo

pantallaHuevo.py
    - Animación de Huevo
    - Crea jugador
    - Avanza a pantallaNombrar

pantallaNombrar.py
    - Input de texto
    - Crea mascota
    - Va a pantallaCasa

pantallaCasa.py
Pantalla principal del juego.
    Muestra:
        - fondo (dia/noche)
        - mascota según estado (feliz, dormido, jugando, enfermo…)
        - botones de acción
Tiene popup cuando está enferma

pantallaHospital.py
    - Muestra la mascota internada
    - Llama a curar_en_hospital()
    - Cuando sana → vuelve a la casa

pantallaLiberacion.py
    - Pantalla final de despedida
    - Guarda mascota en historial
    - Resetea campo.mascota
    - Devuelve a pantallaInicio

pantallaHistorial.py
    - Tabla visual con todas las mascotas liberadas
    - Información: nombre + especie
    - Botón volver

-------------------------------------------------------------------
📦 Dependencias
-------------------------------------------------------------------
pygame
pytest

-------------------------------------------------------------------
🛠️ Fortalezas de PawPop
-------------------------------------------------------------------

    - Arquitectura clara: backend vs frontend.
    - Separación de lógica y UI.
    - Persistencia en JSON.
    - Pantallas bien organizadas.
    - Estados de mascota muy bien definidos.
    - Muchos assets y diseño visual personalizado.