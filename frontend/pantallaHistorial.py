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
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_historial():
    reloj = pygame.time.Clock()

    mascotas = obtener_mascotas_liberadas()  # ✅ usamos backend
    liberadas = [m for m in mascotas if m.get("estado") == "liberada"]

    while True:
        VENTANA.fill(FONDO)

        dibujar_texto("Historial de Mascotas Liberadas", fuente_titulo, TEXTO, 150, 50)

        # Encabezados tabla
        dibujar_texto("Nombre", fuente_tabla, TEXTO, 200, 150)
        dibujar_texto("Tipo", fuente_tabla, TEXTO, 450, 150)

        # Filas
        y = 190
        for m in liberadas:
            dibujar_texto(m["nombre"], fuente_tabla, TEXTO, 200, y)
            dibujar_texto(m["especie"], fuente_tabla, TEXTO, 450, y)
            y += 40

        # Botón volver
        pygame.draw.rect(VENTANA, VERDE, boton_volver, border_radius=8)
        pygame.draw.rect(VENTANA, TEXTO, boton_volver, 2, border_radius=8)
        dibujar_texto("Volver", fuente_boton, TEXTO, boton_volver.x + 30, boton_volver.y + 5)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_huevo()
                    return

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_historial()
