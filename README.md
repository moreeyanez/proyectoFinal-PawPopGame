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
📦 Importaciones/Estructura de datos
-------------------------------------------------------------------
pygame
Librería principal para el desarrollo del juego. Permite crear ventanas, manejar eventos del teclado y mouse, controlar fotogramas, dibujar gráficos, reproducir sonidos y gestionar toda la lógica visual y multimedia del proyecto. Es imprescindible para construir la interfaz y el comportamiento interactivo del juego.

sys
Proporciona funciones relacionadas con el intérprete de Python. Se utiliza principalmente para finalizar el programa de forma segura (sys.exit()), así como para manejar rutas y configuraciones internas necesarias durante la ejecución.
    Caso de uso => Salir del programa correctamente cuando el usuario cierra la ventana (sys.exit())

os
Permite interactuar con el sistema operativo. Se emplea para gestionar rutas de archivos, acceder a recursos del proyecto (imágenes, sonidos), y organizar archivos de forma independiente del sistema (Windows, Linux, etc.) mediante funciones como os.path.join().
    Caso de uso => Permitir importar módulos como backend.controlador y frontend.pantallaHuevo sin errores.

math
Proporciona funciones matemáticas avanzadas utilizadas en cálculos del juego, como distancias, ángulos, movimientos y operaciones geométricas necesarias para el comportamiento de los personajes y elementos del entorno.
    Caso de uso => Para crear efectos de pulso o fade-in/fade-out. (dibujar_titulo_animado())

re
Módulo de expresiones regulares usado para buscar, validar o manipular cadenas de texto siguiendo patrones específicos. Facilita validar entradas, procesar texto estructurado o realizar reemplazos avanzados.
    Caso de uso => Se usa exclusivamente para validar el email antes de continuar. (re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', mail))

random
La librería random permite generar valores aleatorios en Python. Es muy usada en juegos para crear variación, sorpresa y elementos no repetitivos.
    Caso de uso => Para ubicar emojis decorativos en pantalla sin que se superpongan con la UI.

deque
deque (double-ended queue) es una estructura de datos incluida en el módulo collections que funciona como una lista optimizada para agregar y quitar elementos tanto al principio como al final de manera muy rápida.
    Caso de uso => implementamos el historial de acciones con deque(maxlen=5) para mantener las últimas 5 entradas; así agregamos y removemos entradas sin penalizar rendimiento y con comportamiento FIFO/LIFO según convenga.

json
encoder/decoder para el formato JSON (JavaScript Object Notation), estándar ligero para intercambio y persistencia de datos.
    Caso de uso => guardamos el estado de la mascota (un diccionario con nombre, especie, energía, etc.) en un archivo estado_mascota.json y lo leemos al iniciar; json.dump y json.load facilitan esto sin dependencias externas.

-------------------------------------------------------------------
🛠️ Fortalezas de PawPop
-------------------------------------------------------------------

    - Arquitectura clara: backend vs frontend.
    - Separación de lógica y UI.
    - Persistencia en JSON.
    - Pantallas bien organizadas.
    - Estados de mascota muy bien definidos.
    - Muchos assets y diseño visual personalizado.