"""
Pantalla de inicio del juego PawPop.

Esta pantalla permite al usuario ingresar su nombre y su mail para crear su perfil
antes de comenzar la aventura. Incluye:

- Fondo animado con transición de colores.
- Efectos visuales con emojis y huellitas dinámicas.
- Campos interactivos de texto para nombre y mail.
- Botón para avanzar al juego.
- Validación básica antes de continuar.
- Llamada a `crear_jugador()` y transición a la pantalla del huevo.

La función principal de este módulo es `pantalla_inicio()`, que controla el ciclo
principal de eventos y renderizado hasta que el usuario avanza a la siguiente pantalla.
"""

import pygame
import sys, os, random, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import crear_jugador
from frontend.pantallaHuevo import pantalla_huevo
import re

pygame.init()


ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Bienvenido")


VERDE = (156, 138, 97)
CELESTE = (140, 155, 140)
MARRON = (170, 122, 70)
TEXTO = (82, 50, 24)

fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)
fuente_input = pygame.font.SysFont("Arial", 24)
fuente_huella = pygame.font.SysFont("Segoe UI Emoji", 36)
fuente_funny = pygame.font.SysFont("Segoe UI Emoji", 28)


nombre = ""
mail = ""
activo_nombre = False
activo_mail = False
color_nombre = MARRON
color_mail = MARRON

rect_nombre   = pygame.Rect(250, 250, 300, 40)
rect_mail     = pygame.Rect(250, 320, 300, 40)
rect_ingresar = pygame.Rect(325, 400, 150, 50)


rect_titulo     = pygame.Rect(150, 100, 500, 60)
rect_subtitulo  = pygame.Rect(280, 200, 260, 40)
UI_ZONAS = [rect_titulo, rect_subtitulo, rect_nombre, rect_mail, rect_ingresar]


def dibujar_fondo_animado(tiempo):
    """
    Dibuja un fondo animado que cambia de color de manera suave.

    Parámetros:
    tiempo : int
    Tiempo actual del juego (obtenido con pygame.time.get_ticks()), utilizado para calcular el factor de transición entre colores.

    Descripción:
    La función realiza un gradiente animado entre dos colores pastel,
    generando un efecto dinámico y agradable visualmente en la pantalla.

    Retorno: None (Solo dibuja sobre la ventana principal)
    """
    color1 = (222, 184, 135) 
    color2 = (210, 180, 140) 

    factor = (pygame.time.get_ticks() // 10) % 255 / 255
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    VENTANA.fill((r, g, b))


def dibujar_titulo_animado(texto, fuente, color, x, y, tiempo):
    """
    Dibuja un texto con un efecto de pulsación animada.

    Parámetros
    texto : str
        Texto a renderizar.
    fuente : pygame.font.Font
        Fuente utilizada para renderizar el texto.
    color : tuple
        Color del texto en formato RGB.
    x, y : int
        Posición donde se dibuja el texto.
    tiempo : int
        Tiempo usado para calcular la animación del pulso.

    Descripción
    Se escala suavemente el texto usando una función seno para crear
    un efecto de “latido”.
    """
    scale = 1 + 0.05 * math.sin(tiempo * 0.005)  
    superficie = fuente.render(texto, True, color)
    superficie = pygame.transform.rotozoom(superficie, 0, scale)
    VENTANA.blit(superficie, (x, y))

def dibujar_texto(texto, fuente, color, x, y):
    """
    Renderiza un texto simple en la pantalla.

    Parámetros:
    texto : str
        El contenido del texto.
    fuente : pygame.font.Font
        Fuente usada para renderizarlo.
    color : tuple
        Color RGB.
    x, y : int
        Posición donde se mostrará.
    """
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))


def dibujar_boton(rect, texto, activo=False):
    """
    Dibuja un botón interactivo en pantalla.

    Parámetros:
    rect : pygame.Rect
        Rectángulo que define la posición y tamaño del botón.
    texto : str
        Texto que aparece dentro del botón.
    activo : bool, opcional
        Indica si el botón está siendo hovereado por el mouse.

    Descripción
    - Si está activo, muestra un color más claro y un emoji decorativo.
    - El texto del botón se centra automáticamente.
    """
    color = (200, 240, 200) if activo else VERDE
    pygame.draw.rect(VENTANA, color, rect, border_radius=8)
    superficie = fuente_label.render(texto, True, TEXTO)
    VENTANA.blit(superficie, (rect.x + (rect.width - superficie.get_width()) // 2,
                              rect.y + (rect.height - superficie.get_height()) // 2))
    if activo:
        emoji = fuente_funny.render("🐶", True, TEXTO)
        VENTANA.blit(emoji, (rect.right + 10, rect.centery - emoji.get_height() // 2))


def generar_posiciones_emojis(cantidad=8):
    """
    Genera posiciones aleatorias para emojis decorativos en pantalla,
    evitando que se superpongan con zonas de la interfaz.

    Parámetros
    cantidad : int, opcional
        Número de emojis a generar.

    Retorno
    list[tuple[int, int]]
        Lista de posiciones válidas (x, y).
    """
    posiciones = []
    while len(posiciones) < cantidad:
        x = random.randint(30, ANCHO - 50)
        y = random.randint(140, ALTO - 50)
        rect_em = pygame.Rect(x, y, 40, 40)
        if any(rect_em.colliderect(r) for r in UI_ZONAS):
            continue
        posiciones.append((x, y))
    return posiciones

posiciones_emojis = generar_posiciones_emojis()

def dibujar_huellita_emojis(tiempo, posiciones):
    """
    Dibuja emojis de huellitas con un efecto de aparición y desvanecimiento.

    Parámetros
    tiempo : int
        Tiempo actual usado para animar el alpha.
    posiciones : list[tuple[int, int]]
        Posiciones donde dibujar cada emoji.

    Descripción
    Cada huella cambia su transparencia con una función seno,
    creando un efecto visual dinámico.
    """
    alpha = int(70 * math.sin(tiempo * 0.002) + 110)  # Fade in/out efecto :)
    for (x, y) in posiciones:
        superficie = fuente_huella.render("🐾", True, TEXTO)
        superficie.set_alpha(alpha)
        VENTANA.blit(superficie, (x, y))


def emoji_sorpresa():
    """
    Devuelve un emoji aleatorio para efectos decorativos.

    Retorno
    str
        Un emoji seleccionado al azar.
    """
    lista = ["🐶","🐱","🐾","🐢","🐰","🐹","🐸","🐥","🌸","⭐"]
    return random.choice(lista)

emoji_actual = None
emoji_pos = (700, 500)

def dibujar_emoji_sorpresa():
    """
    Dibuja el emoji sorpresa si existe uno seleccionado.

    Descripción:
    El emoji aparece con leve transparencia en su posición fija.
    """
    global emoji_actual
    if emoji_actual:
        superficie = fuente_huella.render(emoji_actual, True, TEXTO)
        superficie.set_alpha(220)
        VENTANA.blit(superficie, emoji_pos)

error_mail = ""
fuente_error = pygame.font.SysFont("Arial", 20)


def pantalla_inicio():
    """
    Pantalla inicial del juego donde el usuario ingresa su nombre y mail.

    Funcionalidad
    - Fondo animado y efectos visuales.
    - Campos interactivos para completar datos.
    - Botón para ingresar al juego.
    - Generación de emojis sorpresa al escribir o hacer clic.
    - Llamada a la función `crear_jugador` y luego a `pantalla_huevo()`.

    Manejo de eventos
    - Clics en los campos de texto para activarlos.
    - Escritura de caracteres.
    - Validación básica antes de continuar.
    - Cierre de la ventana.

    Retorno: None (La función no retorna valores; navega hacia otra pantalla)
    """
    global nombre, mail, activo_nombre, activo_mail, color_nombre, color_mail, emoji_actual, error_mail
    reloj = pygame.time.Clock()

    while True:
        tiempo = pygame.time.get_ticks()
        dibujar_fondo_animado(tiempo)
        dibujar_huellita_emojis(tiempo, posiciones_emojis)
        dibujar_emoji_sorpresa()

        
        dibujar_titulo_animado("¡Bienvenido a PawPop!", fuente_titulo, TEXTO, rect_titulo.x, rect_titulo.y, tiempo)
        dibujar_texto("Ingresa tus datos", fuente_label, TEXTO, rect_subtitulo.x, rect_subtitulo.y)

        
        pygame.draw.rect(VENTANA, color_nombre, rect_nombre, 2)
        pygame.draw.rect(VENTANA, color_mail, rect_mail, 2)

        dibujar_texto(nombre, fuente_input, TEXTO, rect_nombre.x + 10, rect_nombre.y + 5)
        dibujar_texto(mail, fuente_input, TEXTO, rect_mail.x + 10, rect_mail.y + 5)

        dibujar_texto("Nombre:", fuente_label, TEXTO, 150, 255)
        dibujar_texto("Mail:",    fuente_label, TEXTO, 150, 325)

        
        hover_ingresar = rect_ingresar.collidepoint(pygame.mouse.get_pos())
        dibujar_boton(rect_ingresar, "Ingresar", activo=hover_ingresar)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                activo_nombre = rect_nombre.collidepoint(evento.pos)
                activo_mail   = rect_mail.collidepoint(evento.pos)
                if rect_ingresar.collidepoint(evento.pos):
                    if nombre and mail:
                        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', mail):
                            error_mail = "El mail no tiene un formato válido."
                        else:
                            error_mail = ""
                            emoji_actual = emoji_sorpresa()
                            try:
                                crear_jugador(nombre, mail)
                                pantalla_huevo()
                                return
                            except ValueError as e:
                                error_mail = str(e)

            if evento.type == pygame.KEYDOWN:
                if activo_nombre:
                    if evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode
                        emoji_actual = emoji_sorpresa() 
                elif activo_mail:
                    if evento.key == pygame.K_BACKSPACE:
                        mail = mail[:-1]
                    else:
                        mail += evento.unicode
                        emoji_actual = emoji_sorpresa() 

        color_nombre = CELESTE if activo_nombre else MARRON
        color_mail   = CELESTE if activo_mail   else MARRON
        
        if error_mail:
            dibujar_texto(error_mail, fuente_error, (200, 50, 50), 250, 370)

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_inicio()



