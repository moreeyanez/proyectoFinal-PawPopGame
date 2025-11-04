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
especies = ["Perro", "Gato", "Vaca", "Capibara", "Conejo"]
espaciado = 120
inicio_x = (ANCHO - (espaciado * len(especies))) // 2 + 60

for i, especie in enumerate(especies):
    x = inicio_x + i * espaciado
    boton = pygame.Rect(x, 450, 100, 40)
    botones.append((boton, especie))

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_huevo():
    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)

        dibujar_texto("Elegí tu mascota", fuente_titulo, TEXTO, 220, 50)
        
        if imagen_huevito:
            VENTANA.blit(imagen_huevito, (ANCHO // 2 - 100, 150))

        for boton, especie in botones:
            pygame.draw.rect(VENTANA, VERDE, boton)
            dibujar_texto(especie, fuente_boton, TEXTO, boton.x + 10, boton.y + 8)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton, especie in botones:
                    if boton.collidepoint(evento.pos):
                        try:
                            crear_mascota("Mascota", especie)  
                            print(f"Mascota {especie} creada con éxito.")
                            
                        except Exception as e:
                            print("Error al crear mascota:", e)

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_huevo()