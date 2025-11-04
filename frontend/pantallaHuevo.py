import pygame
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import crear_mascota

pygame.init()


# VENTANA
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Elegí tu mascota")


# COLORES
FONDO = (255, 248, 226)
VERDE = (156, 138, 97)
TEXTO = (82, 50, 24)


# FUENTES
fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_boton = pygame.font.SysFont("Arial", 24)


BASE = os.path.dirname(os.path.abspath(__file__)) 
ruta_huevito = os.path.join(BASE, "..", "assets", "Huevito.png")

try:
    imagen_huevito = pygame.image.load(ruta_huevito)
    imagen_huevito = pygame.transform.scale(imagen_huevito, (200, 250))
except pygame.error as e:
    print("No se pudo cargar la imagen del huevo:", e)
    imagen_huevito = None

# BOTONES
botones = []
especies = ["Perro", "Gato", "Vaca", "Capybara", "Conejo"]
espaciado = 120
inicio_x = (ANCHO - (espaciado * len(especies))) // 2 + 60

for i, especie in enumerate(especies):
    x = inicio_x + i * espaciado
    boton = pygame.Rect(x, 450, 100, 40)
    botones.append((boton, especie))

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_huevo(nombre_mascota):
    reloj = pygame.time.Clock()
    offset = 0
    direccion = 1


    while True:
        VENTANA.fill(FONDO)

        dibujar_texto("Elegí tu mascota", fuente_titulo, TEXTO, 220, 50)
        
        if imagen_huevito:
            # Animación de temblor
            offset += direccion
            if abs(offset) > 5:
                direccion *= -1

            VENTANA.blit(imagen_huevito, (ANCHO // 2 - 100 + offset, 150))

            # VENTANA.blit(imagen_huevito, (ANCHO // 2 - 100, 150))

        for boton, especie in botones:
            # Dibujar botón con borde
            mouse_pos = pygame.mouse.get_pos()
            color_boton = VERDE if not boton.collidepoint(mouse_pos) else (180, 160, 120)

            pygame.draw.rect(VENTANA, color_boton, boton)  # Fondo con hover
            pygame.draw.rect(VENTANA, TEXTO, boton, 2)     # Borde

            # pygame.draw.rect(VENTANA, VERDE, boton)  # Fondo
            # pygame.draw.rect(VENTANA, TEXTO, boton, 2)  # Borde de 2px

            # Centrar texto
            texto_superficie = fuente_boton.render(especie, True, TEXTO)
            texto_rect = texto_superficie.get_rect(center=boton.center)
            VENTANA.blit(texto_superficie, texto_rect)


        # for boton, especie in botones:
        #     pygame.draw.rect(VENTANA, VERDE, boton)
        #     dibujar_texto(especie, fuente_boton, TEXTO, boton.x + 10, boton.y + 8)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton, especie in botones:
                    if boton.collidepoint(evento.pos):
                        try:
                            from backend.controlador import crear_mascota, campo
                            from frontend.pantallaCasa import mostrar_pantalla_casa

                            crear_mascota(nombre_mascota, especie)
                            mascota = campo.mascota
                            mostrar_pantalla_casa(mascota)
                            return  # ← Esto corta el bucle sin cerrar Pygame

                        except Exception as e:
                            print("Error al crear mascota:", e)


        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_huevo()