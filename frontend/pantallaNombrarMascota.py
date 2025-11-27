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
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_nombrar_mascota(especie):
    """
    Recibe la especie elegida en pantallaHuevo.
    El jugador escribe el nombre de la mascota y se crea en el backend.
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
                    # Crear mascota en backend con nombre definitivo
                    crear_mascota(nombre, especie)
                    mascota = campo.mascota

                    # Pasar a pantalla Casa
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
    # Para pruebas rápidas
    pantalla_nombrar_mascota("Perro")

