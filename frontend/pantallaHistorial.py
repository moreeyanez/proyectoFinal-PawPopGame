import pygame
import sys
from backend.controlador import jugador
from frontend.pantallaHuevo import pantalla_huevo

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Historial de Mascotas")

fondo_hospital = pygame.image.load("assets/Hospitalito.png")
fondo_hospital = pygame.transform.scale(fondo_hospital, (ANCHO, ALTO))

# Colores
FONDO = (240, 255, 240)
TEXTO = (50, 80, 30)
BOTON = (150, 200, 150)
LINEA = (100, 150, 100)

fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)

# Botón volver
boton_volver = pygame.Rect(325, 500, 150, 50)

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(fondo_hospital, (0, 0))

def pantalla_historial():
    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)
        dibujar_texto("Historial de Mascotas Liberadas", fuente_titulo, TEXTO, 100, 50)

        # Encabezados de tabla
        dibujar_texto("Nombre", fuente_label, TEXTO, 200, 120)
        dibujar_texto("Especie", fuente_label, TEXTO, 450, 120)

        # Línea separadora
        pygame.draw.line(VENTANA, LINEA, (180, 150), (620, 150), 2)

        # Mostrar mascotas liberadas en filas
        if jugador and jugador.mascotas_liberadas:
            y_offset = 180
            for m in jugador.mascotas_liberadas:
                dibujar_texto(m["nombre"], fuente_label, TEXTO, 200, y_offset)
                dibujar_texto(m["especie"], fuente_label, TEXTO, 450, y_offset)
                y_offset += 40
        else:
            dibujar_texto("No hay mascotas liberadas aún.", fuente_label, TEXTO, 200, 200)

        # Botón volver
        pygame.draw.rect(VENTANA, BOTON, boton_volver)
        dibujar_texto("Volver", fuente_label, TEXTO, boton_volver.x + 40, boton_volver.y + 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    pantalla_huevo()  # volver a pantalla huevo
                    return

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_historial()

