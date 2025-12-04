"""
Pantalla de nombramiento de mascota del juego PawPop.

Este módulo muestra la interfaz donde el jugador ingresa el nombre de la mascota
recién creada. Recibe la especie seleccionada previamente en `pantallaHuevo` y
permite completar el proceso de creación de la mascota.

Características principales:
- Campo de texto interactivo para ingresar el nombre.
- Botón para confirmar y avanzar.
- Integración con el backend para crear la mascota mediante `crear_mascota()`.
- Transición automática hacia la pantalla de la casa (`mostrar_pantalla_casa`)
una vez asignado el nombre.

Funciones principales:
- `pantalla_nombrar_mascota(especie)`: Ejecuta el loop de la pantalla,
renderiza los elementos gráficos e interpreta las acciones del jugador.
"""

import pygame
import sys
from backend.controlador import crear_mascota, campo
from frontend.pantallaCasa import mostrar_pantalla_casa

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Nombrar Mascota")

# Colores
FONDO = (255, 248, 226)
TEXTO = (82, 50, 24)
VERDE = (156, 138, 97)
CELESTE = (140, 155, 140)
MARRON = (170, 122, 70)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)
fuente_input = pygame.font.SysFont("Arial", 24)

# Input
nombre = ""
activo = False
color_input = MARRON
rect_input = pygame.Rect(250, 300, 300, 40)
rect_siguiente = pygame.Rect(325, 400, 150, 50)

def dibujar_texto(texto, fuente, color, x, y):
    """
    Dibuja texto en la ventana del juego.

    Parámetros:
    texto : str
        Cadena que se mostrará en pantalla.
    fuente : pygame.font.Font
        Fuente usada para renderizar el texto.
    color : tuple[int, int, int]
        Color RGB del texto.
    x : int
        Posición horizontal donde se dibujará el texto.
    y : int
        Posición vertical donde se dibujará el texto.
    """
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_nombrar_mascota(especie):
    """
    Muestra la pantalla donde el jugador escribe el nombre de su mascota.

    Parámetros
    especie : str
        La especie seleccionada previamente en pantallaHuevo (por ejemplo,
        "Perro", "Gato", etc.). Se utiliza para crear la mascota en el backend.

    Descripción:
    La pantalla contiene un campo de texto interactivo donde el jugador
    puede escribir el nombre de su mascota. Cuando se presiona el botón
    "Siguiente" y el nombre no está vacío:

    - Se llama a `crear_mascota(nombre, especie)` en el backend.
    - La mascota creada se obtiene desde `campo.mascota`.
    - Se redirige al jugador a la pantalla principal del hogar mediante
      `mostrar_pantalla_casa(mascota)`.

    El loop de la pantalla gestiona:
    - Eventos de teclado para escribir o borrar texto.
    - Detección de clics para activar el input o confirmar el nombre.
    - Renderizado continuo del fondo, textos, botón e input.

    Esta función solo se cierra cuando una mascota válida es creada y se pasa a la siguiente pantalla.
    """
    global nombre, activo, color_input
    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)
        dibujar_texto("Ponle un nombre a tu mascota", fuente_titulo, TEXTO, 80, 200)

        # Input
        pygame.draw.rect(VENTANA, color_input, rect_input, 2)
        dibujar_texto(nombre, fuente_input, TEXTO, rect_input.x + 10, rect_input.y + 5)

        # Botón siguiente
        pygame.draw.rect(VENTANA, VERDE, rect_siguiente)
        dibujar_texto("Siguiente", fuente_label, TEXTO, rect_siguiente.x + 25, rect_siguiente.y + 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                activo = rect_input.collidepoint(evento.pos)
                if rect_siguiente.collidepoint(evento.pos) and nombre:
                    crear_mascota(nombre, especie)
                    mascota = campo.mascota

                    mostrar_pantalla_casa(mascota)
                    return

            if evento.type == pygame.KEYDOWN and activo:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode

        color_input = CELESTE if activo else MARRON
        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_nombrar_mascota("Perro")

