import pygame
import sys
import os
from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego
from frontend.pantallaHuevo import pantalla_huevo

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
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_liberacion():
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
        ver_mascotas_liberadas()  # imprime en consola
        # (Opcional: podríamos capturar el historial y dibujarlo en pantalla)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_liberar.collidepoint(evento.pos):
                    confirmar_liberacion()
                elif boton_nueva.collidepoint(evento.pos):
                    pantalla_huevo("Mascota")  # vuelve al flujo de creación
                    return
                elif boton_salir.collidepoint(evento.pos):
                    salir_del_juego()

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_liberacion()
