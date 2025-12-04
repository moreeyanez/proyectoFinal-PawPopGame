"""
Módulo de la pantalla de liberación del juego PawPop.

Esta pantalla aparece cuando la mascota del jugador ha completado su ciclo y está
lista para ser liberada. El objetivo principal es permitir al usuario decidir entre:

- Liberar definitivamente la mascota y registrarla en el historial.
- Comenzar una nueva mascota desde el huevo.
- Salir del juego.

Además, la pantalla muestra un listado de todas las mascotas liberadas previamente,
utilizando la información almacenada por el backend.

Funciones principales:
- pantalla_liberacion(): administra el loop principal de la pantalla, la interacción
  con los botones y la actualización visual.
- dibujar_texto(): función auxiliar para renderizar texto en pantalla.

Dependencias importantes:
- confirmar_liberacion(): registra una nueva liberación en el backend.
- obtener_mascotas_liberadas(): devuelve el historial de mascotas.
- pantalla_huevo(): permite comenzar la creación de una nueva mascota.
- salir_del_juego(): cierra el juego correctamente.
"""

import pygame
import sys
import os
from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego
from frontend.pantallaHuevo import pantalla_huevo
from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego, obtener_mascotas_liberadas

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Liberación")

# Colores
FONDO = (200, 255, 200)
TEXTO = (50, 80, 30)
BOTON = (150, 200, 150)

fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)

# Botones
boton_liberar = pygame.Rect(150, 450, 150, 50)
boton_nueva = pygame.Rect(325, 450, 150, 50)
boton_salir = pygame.Rect(500, 450, 150, 50)

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

def pantalla_liberacion():
    """
    Ejecuta la pantalla de liberación de la mascota.

    Esta función controla el loop principal de la pantalla, incluyendo:
    - Renderizado del mensaje principal.
    - Dibujado de botones de interacción.
    - Visualización del historial de mascotas liberadas.
    - Manejo de eventos de clic para liberar la mascota, crear una nueva o salir.

    Flujo de opciones:
    - "Liberar": llama a `confirmar_liberacion()` y vuelve a pantalla_huevo().
    - "Nueva Mascota": reinicia el proceso creando un nuevo huevo.
    - "Salir": ejecuta `salir_del_juego()`.

    El loop continúa hasta que el usuario selecciona alguna acción válida.
    """
    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)
        dibujar_texto("Tu mascota está lista para ser liberada", fuente_titulo, TEXTO, 80, 100)

        # Botones
        pygame.draw.rect(VENTANA, BOTON, boton_liberar)
        pygame.draw.rect(VENTANA, BOTON, boton_nueva)
        pygame.draw.rect(VENTANA, BOTON, boton_salir)

        dibujar_texto("Liberar", fuente_label, TEXTO, boton_liberar.x + 25, boton_liberar.y + 10)
        dibujar_texto("Nueva Mascota", fuente_label, TEXTO, boton_nueva.x + 5, boton_nueva.y + 10)
        dibujar_texto("Salir", fuente_label, TEXTO, boton_salir.x + 50, boton_salir.y + 10)

        # Mostrar historial de mascotas liberadas
        dibujar_texto("Mascotas liberadas:", fuente_label, TEXTO, 80, 200)

        mascotas = obtener_mascotas_liberadas()
        y_offset = 250
        for m in mascotas:
            texto = f"- {m['nombre']} ({m['especie']})"
            dibujar_texto(texto, fuente_label, TEXTO, 100, y_offset)
            y_offset += 30
        # (Opcional: podríamos capturar el historial y dibujarlo en pantalla)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_liberar.collidepoint(evento.pos):
                    confirmar_liberacion()
                    pantalla_huevo()
                    return
                elif boton_nueva.collidepoint(evento.pos):
                    pantalla_huevo("Mascota")  # vuelve al flujo de creación
                    return
                elif boton_salir.collidepoint(evento.pos):
                    salir_del_juego()
                    return

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_liberacion()
