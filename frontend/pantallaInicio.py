import pygame
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import crear_jugador

from frontend.pantallaHuevo import pantalla_huevo


pygame.init()

#VENTANA
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Bienvenido")


#ESTILOS
FONDO = (237, 221, 185)
AMARILLO = (255, 229, 180)
VERDE = (156, 138, 97)
CELESTE = (140, 155, 140)
MARRON = (170, 122, 70)
TEXTO = (82, 50, 24)

fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)
fuente_input = pygame.font.SysFont("Arial", 24)


#FORM
nombre = ""
mail = ""
activo_nombre = False
activo_mail = False
color_nombre = MARRON
color_mail = MARRON

rect_nombre = pygame.Rect(250, 250, 300, 40)
rect_mail = pygame.Rect(250, 320, 300, 40)
rect_ingresar = pygame.Rect(325, 400, 150, 50)


def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_inicio():
    global nombre, mail, activo_nombre, activo_mail, color_nombre, color_mail

    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)
        dibujar_texto("¡Bienvenido a PawPop!", fuente_titulo, TEXTO, 150, 100)

        dibujar_texto("Ingresa tus datos", fuente_label, TEXTO, 280, 200)

        pygame.draw.rect(VENTANA, color_nombre, rect_nombre, 2)
        pygame.draw.rect(VENTANA, color_mail, rect_mail, 2)
        pygame.draw.rect(VENTANA, VERDE, rect_ingresar)

        dibujar_texto(nombre, fuente_input, TEXTO, rect_nombre.x + 10, rect_nombre.y + 5)
        dibujar_texto(mail, fuente_input, TEXTO, rect_mail.x + 10, rect_mail.y + 5)
        
        dibujar_texto("Nombre:", fuente_label, TEXTO, 150, 255)
        dibujar_texto("Mail:", fuente_label, TEXTO, 150, 325)

        dibujar_texto("Ingresar", fuente_label, TEXTO, rect_ingresar.x + 25, rect_ingresar.y + 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                activo_nombre = rect_nombre.collidepoint(evento.pos)
                activo_mail = rect_mail.collidepoint(evento.pos)
                if rect_ingresar.collidepoint(evento.pos):
                    if nombre and mail:
                        try:
                            # Crear jugador con nombre y mail
                            crear_jugador(nombre, mail)

                            # Pasar a pantalla de elección de mascota (no se pasa nombre aquí)
                            pantalla_huevo()

                        except ValueError as e:
                            print("Error:", e)


            if evento.type == pygame.KEYDOWN:
                if activo_nombre:
                    if evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode
                elif activo_mail:
                    if evento.key == pygame.K_BACKSPACE:
                        mail = mail[:-1]
                    else:
                        mail += evento.unicode

        color_nombre = CELESTE if activo_nombre else MARRON
        color_mail = CELESTE if activo_mail else MARRON

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_inicio()