"""
Pantalla de historial de mascotas liberadas del juego PawPop.

Este módulo muestra una interfaz dedicada a visualizar la lista de mascotas
que han sido liberadas a lo largo del juego. Obtiene la información desde el
backend mediante `obtener_mascotas_liberadas()` y renderiza los datos en una
tabla simple con nombre y especie de cada mascota.

Características principales
---------------------------
- Renderización del historial de mascotas liberadas, filtrando únicamente
  aquellas cuyo estado sea "liberada".
- Presentación organizada en formato de tabla (Nombre / Tipo).
- Botón para regresar a la pantalla del huevo (`pantalla_huevo`).
- Bucle principal que gestiona eventos, entrada del jugador y refresco visual.

Estructura
----------
Funciones:
- `dibujar_texto()`: Utilidad para renderizar texto en pantalla.
- `pantalla_historial()`: Controla la visualización completa del historial,
  administra eventos y permite volver a la pantalla anterior.

Este módulo forma parte del flujo principal del juego y se utiliza para que
el jugador pueda consultar todas sus mascotas liberadas hasta el momento.
"""

import pygame
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import obtener_mascotas_liberadas
from frontend.pantallaHuevo import pantalla_huevo

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Historial")

FONDO = (240, 230, 200)
TEXTO = (82, 50, 24)
VERDE = (156, 138, 97)

fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_tabla = pygame.font.SysFont("Arial", 24)
fuente_boton = pygame.font.SysFont("Arial", 28)

boton_volver = pygame.Rect(325, 520, 150, 40)

def dibujar_texto(texto, fuente, color, x, y):
    """
    Renderiza y dibuja texto sobre la ventana principal.

    Parámetros
    ----------
    texto : str
        Cadena que se mostrará en pantalla.
    fuente : pygame.font.Font
        Fuente utilizada para renderizar el texto.
    color : tuple
        Color en formato RGB.
    x : int
        Posición horizontal donde se dibujará el texto.
    y : int
        Posición vertical donde se dibujará el texto.
    """

    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_historial():
    """
    Muestra la pantalla de historial de mascotas liberadas.

    - Obtiene el historial desde el backend.
    - Renderiza una tabla con nombre y tipo de cada mascota liberada.
    - Incluye un botón para volver a la pantalla del huevo.
    - Se mantiene en un bucle hasta que el usuario regresa o cierra la ventana.

    Esta función constituye una pantalla completa dentro del flujo del juego.
    """
    reloj = pygame.time.Clock()

    # Obtener mascotas liberadas desde backend
    mascotas = obtener_mascotas_liberadas() 
    liberadas = [m for m in mascotas if m.get("estado") == "liberada"]

    while True:
        VENTANA.fill(FONDO)

        # Título principal
        dibujar_texto("Historial de Mascotas Liberadas", fuente_titulo, TEXTO, 150, 50)

        # Encabezados de la tabla
        dibujar_texto("Nombre", fuente_tabla, TEXTO, 200, 150)
        dibujar_texto("Tipo", fuente_tabla, TEXTO, 450, 150)

        # Contenido de la tabla
        y = 190
        for m in liberadas:
            dibujar_texto(m["nombre"], fuente_tabla, TEXTO, 200, y)
            dibujar_texto(m["especie"], fuente_tabla, TEXTO, 450, y)
            y += 40

        # Botón volver
        pygame.draw.rect(VENTANA, VERDE, boton_volver, border_radius=8)
        pygame.draw.rect(VENTANA, TEXTO, boton_volver, 2, border_radius=8)
        dibujar_texto("Volver", fuente_boton, TEXTO, boton_volver.x + 30, boton_volver.y + 5)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_huevo()
                    return # Volver a pantalla anterior

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_historial()
