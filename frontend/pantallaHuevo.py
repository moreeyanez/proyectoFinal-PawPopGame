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

boton_historial = pygame.Rect(325, 520, 150, 40)

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_huevo():
    reloj = pygame.time.Clock()
    offset = 0
    direccion = 1


    while True:
        VENTANA.fill(FONDO)

        dibujar_texto("Elegí tu mascota", fuente_titulo, TEXTO, 220, 50)
        
        if imagen_huevito:
            offset += direccion
            if abs(offset) > 5:
                direccion *= -1

            VENTANA.blit(imagen_huevito, (ANCHO // 2 - 100 + offset, 150))


        for boton, especie in botones:
            mouse_pos = pygame.mouse.get_pos()
            color_boton = VERDE if not boton.collidepoint(mouse_pos) else (180, 160, 120)

            pygame.draw.rect(VENTANA, color_boton, boton)
            pygame.draw.rect(VENTANA, TEXTO, boton, 2)
            pygame.draw.rect(VENTANA, VERDE, boton_historial)
            dibujar_texto("Historial", fuente_boton, TEXTO, boton_historial.x + 25, boton_historial.y + 10)
 
            texto_superficie = fuente_boton.render(especie, True, TEXTO)
            texto_rect = texto_superficie.get_rect(center=boton.center)
            VENTANA.blit(texto_superficie, texto_rect)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton, especie in botones:
                    if boton.collidepoint(evento.pos):
                        try:
                            from frontend.pantallaNombrarMascota import pantalla_nombrar_mascota
                            pantalla_nombrar_mascota(especie)  # solo especie
                            return
                        except Exception as e:
                            print("Error al elegir especie:", e)
                    
                    if boton_historial.collidepoint(evento.pos):
                        from frontend.pantallaHistorial import pantalla_historial
                        pantalla_historial()
                        return

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_huevo()