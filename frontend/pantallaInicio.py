import pygame
import sys, os, random, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controlador import crear_jugador
from frontend.pantallaHuevo import pantalla_huevo

pygame.init()

# VENTANA
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Bienvenido")

# ESTILOS
VERDE = (156, 138, 97)
CELESTE = (140, 155, 140)
MARRON = (170, 122, 70)
TEXTO = (82, 50, 24)

fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)
fuente_input = pygame.font.SysFont("Arial", 24)
fuente_huella = pygame.font.SysFont("Segoe UI Emoji", 36)
fuente_funny = pygame.font.SysFont("Segoe UI Emoji", 28)

# FORM
nombre = ""
mail = ""
activo_nombre = False
activo_mail = False
color_nombre = MARRON
color_mail = MARRON

rect_nombre   = pygame.Rect(250, 250, 300, 40)
rect_mail     = pygame.Rect(250, 320, 300, 40)
rect_ingresar = pygame.Rect(325, 400, 150, 50)

# Zonas prohibidas para huellas
rect_titulo     = pygame.Rect(150, 100, 500, 60)
rect_subtitulo  = pygame.Rect(280, 200, 260, 40)
UI_ZONAS = [rect_titulo, rect_subtitulo, rect_nombre, rect_mail, rect_ingresar]

# --- Fondo animado ---
def dibujar_fondo_animado(tiempo):
    color1 = (135, 206, 250)   # celeste brillante
    color2 = (255, 182, 193)   # rosa pastel
    factor = (pygame.time.get_ticks() // 10) % 255 / 255
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    VENTANA.fill((r, g, b))

# --- Animación de título ---
def dibujar_titulo_animado(texto, fuente, color, x, y, tiempo):
    scale = 1 + 0.05 * math.sin(tiempo * 0.005)  # pulso suave
    superficie = fuente.render(texto, True, color)
    superficie = pygame.transform.rotozoom(superficie, 0, scale)
    VENTANA.blit(superficie, (x, y))

def dibujar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

# --- Botón con hover funny ---
def dibujar_boton(rect, texto, activo=False):
    color = (200, 240, 200) if activo else VERDE
    pygame.draw.rect(VENTANA, color, rect, border_radius=8)
    superficie = fuente_label.render(texto, True, TEXTO)
    VENTANA.blit(superficie, (rect.x + (rect.width - superficie.get_width()) // 2,
                              rect.y + (rect.height - superficie.get_height()) // 2))
    if activo:
        emoji = fuente_funny.render("🐶", True, TEXTO)
        VENTANA.blit(emoji, (rect.right + 10, rect.centery - emoji.get_height() // 2))

# --- Huellitas emoji ---
def generar_posiciones_emojis(cantidad=8):
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
    alpha = int(70 * math.sin(tiempo * 0.002) + 110)  # fade in/out
    for (x, y) in posiciones:
        superficie = fuente_huella.render("🐾", True, TEXTO)
        superficie.set_alpha(alpha)
        VENTANA.blit(superficie, (x, y))

# --- Emoji sorpresa ---
def emoji_sorpresa():
    lista = ["🐶","🐱","🐾","🐢","🐰","🐹","🐸","🐥","🌸","⭐"]
    return random.choice(lista)

emoji_actual = None
emoji_pos = (700, 500)

def dibujar_emoji_sorpresa():
    global emoji_actual
    if emoji_actual:
        superficie = fuente_huella.render(emoji_actual, True, TEXTO)
        superficie.set_alpha(220)
        VENTANA.blit(superficie, emoji_pos)

# --- Pantalla principal ---
def pantalla_inicio():
    global nombre, mail, activo_nombre, activo_mail, color_nombre, color_mail, emoji_actual
    reloj = pygame.time.Clock()

    while True:
        tiempo = pygame.time.get_ticks()
        dibujar_fondo_animado(tiempo)
        dibujar_huellita_emojis(tiempo, posiciones_emojis)
        dibujar_emoji_sorpresa()

        # Título animado
        dibujar_titulo_animado("¡Bienvenido a PawPop!", fuente_titulo, TEXTO, rect_titulo.x, rect_titulo.y, tiempo)
        dibujar_texto("Ingresa tus datos", fuente_label, TEXTO, rect_subtitulo.x, rect_subtitulo.y)

        # Inputs
        pygame.draw.rect(VENTANA, color_nombre, rect_nombre, 2)
        pygame.draw.rect(VENTANA, color_mail, rect_mail, 2)

        dibujar_texto(nombre, fuente_input, TEXTO, rect_nombre.x + 10, rect_nombre.y + 5)
        dibujar_texto(mail, fuente_input, TEXTO, rect_mail.x + 10, rect_mail.y + 5)

        dibujar_texto("Nombre:", fuente_label, TEXTO, 150, 255)
        dibujar_texto("Mail:",    fuente_label, TEXTO, 150, 325)

        # Botón con hover funny
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
                        emoji_actual = emoji_sorpresa()  # emoji sorpresa al click
                        try:
                            crear_jugador(nombre, mail)
                            pantalla_huevo()
                        except ValueError as e:
                            print("Error:", e)

            if evento.type == pygame.KEYDOWN:
                if activo_nombre:
                    if evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode
                        emoji_actual = emoji_sorpresa()  # emoji sorpresa al escribir
                elif activo_mail:
                    if evento.key == pygame.K_BACKSPACE:
                        mail = mail[:-1]
                    else:
                        mail += evento.unicode
                        emoji_actual = emoji_sorpresa()  # emoji sorpresa al escribir

        color_nombre = CELESTE if activo_nombre else MARRON
        color_mail   = CELESTE if activo_mail   else MARRON

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_inicio()



