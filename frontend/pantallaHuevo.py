"""
Pantalla del huevo del juego PawPop.

En esta pantalla el jugador interactúa con su huevo inicial, donde comienza la
experiencia principal del juego. Aquí pueden mostrarse animaciones, efectos,
interacciones y acciones que preparan al jugador para la etapa de crianza
del personaje.

Funcionalidades típicas de esta pantalla incluyen:

- Mostrar el huevo con animación o estados.
- Detectar clics o acciones del jugador.
- Reproducir efectos visuales.
- Controlar el avance hacia la siguiente etapa del juego.

La función principal del módulo es `pantalla_huevo()`, la cual administra el
loop de renderizado y eventos mientras esta pantalla está activa.
"""


import pygame
import sys
import os
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import crear_mascota

pygame.init()

# Ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Elegí tu mascota")

# Colores
FONDO = (255, 248, 226)
VERDE = (156, 138, 97)
TEXTO = (82, 50, 24)

# Tipografías
fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_boton = pygame.font.SysFont("Arial", 24)

# Cargar imagen del huevo
BASE = os.path.dirname(os.path.abspath(__file__)) 
ruta_huevito = os.path.join(BASE, "..", "assets", "Huevito.png")

try:
    imagen_huevito = pygame.image.load(ruta_huevito)
    imagen_huevito = pygame.transform.scale(imagen_huevito, (200, 250))
except pygame.error as e:
    print("No se pudo cargar la imagen del huevo:", e)
    imagen_huevito = None

# Botones de especies
botones = []
especies = ["Perro", "Gato", "Vaca", "Capibara", "Conejo"]
espaciado = 120
inicio_x = (ANCHO - (espaciado * len(especies))) // 2 + 60

for i, especie in enumerate(especies):
    x = inicio_x + i * espaciado
    boton = pygame.Rect(x, 450, 100, 40)
    botones.append((boton, especie))

# Botón historial
boton_historial = pygame.Rect(325, 520, 150, 40)

# Botón salir
boton_salir = pygame.Rect(50, 520, 100, 40)


def dibujar_texto(texto, fuente, color, x, y):
    '''
    Renderiza y dibuja un texto en la ventana principal del juego.
    Parámetros:

    - texto: Cadena de texto a renderizar.
    - fuente: Objeto de fuente de Pygame.
    - color: Tupla RGB del color del texto.
    - x, y: Coordenadas donde se dibujará el texto.
    '''

    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def animar_huevito(tiempo):
    '''
    Realiza la animación del huevito aplicando un movimiento oscilatorio horizontal.
    La función únicamente dibuja el huevo animado en la ventana.
    '''

    if imagen_huevito:
        offset_x = int(10 * math.sin(tiempo * 0.005))
        huevo = imagen_huevito.copy()
        VENTANA.blit(huevo, (ANCHO // 2 - 100 + offset_x, 150))

def pantalla_huevo():
    '''
     Pantalla principal donde el usuario elige la especie de su mascota.

    Esta función administra:
    - El renderizado del título y del huevito animado.
    - La creación y visualización de botones de especies.
    - El acceso al historial de mascotas.
    - El botón para salir del juego.
    - La detección de eventos del mouse y navegación a otras pantallas.
    '''
    reloj = pygame.time.Clock()

    while True:
        tiempo = pygame.time.get_ticks()
        VENTANA.fill(FONDO)

        # Título
        dibujar_texto("Elegí tu mascota", fuente_titulo, TEXTO, 220, 50)

        # Huevito animado
        animar_huevito(tiempo)

        # Botones de especies
        for boton, especie in botones:
            mouse_pos = pygame.mouse.get_pos()
            color_boton = VERDE if not boton.collidepoint(mouse_pos) else (200, 180, 140)

            pygame.draw.rect(VENTANA, color_boton, boton, border_radius=8)
            pygame.draw.rect(VENTANA, TEXTO, boton, 2, border_radius=8)

            texto_superficie = fuente_boton.render(especie, True, TEXTO)
            texto_rect = texto_superficie.get_rect(center=boton.center)
            VENTANA.blit(texto_superficie, texto_rect)

        # Botón historial
        pygame.draw.rect(VENTANA, VERDE, boton_historial, border_radius=8)
        pygame.draw.rect(VENTANA, TEXTO, boton_historial, 2, border_radius=8)
        dibujar_texto("Historial", fuente_boton, TEXTO,
                      boton_historial.x + 25, boton_historial.y + 10)
        
        # Botón salir
        pygame.draw.rect(VENTANA, VERDE, boton_salir, border_radius=8)
        pygame.draw.rect(VENTANA, TEXTO, boton_salir, 2, border_radius=8)
        dibujar_texto("Salir", fuente_boton, TEXTO, boton_salir.x + 20, boton_salir.y + 8)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton, especie in botones:
                    if boton.collidepoint(evento.pos):
                        try:
                            from frontend.pantallaNombrarMascota import pantalla_nombrar_mascota
                            pantalla_nombrar_mascota(especie)
                            return
                        except Exception as e:
                            print("Error al elegir especie:", e)

                if boton_historial.collidepoint(evento.pos):
                    try:
                        from frontend.pantallaHistorial import pantalla_historial
                        pantalla_historial()
                        return
                    except Exception as e:
                        print("Error al abrir historial:", e)
                        
                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()


        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_huevo()
