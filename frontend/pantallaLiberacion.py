"""
Módulo de la pantalla de liberación del juego PawPop.

Esta pantalla aparece cuando la mascota del jugador ha completado su ciclo y está
lista para ser liberada. El objetivo principal es permitir al usuario decidir entre:

- Liberar definitivamente la mascota y registrarla en el historial.
- Comenzar una nueva mascota desde el huevo.
- Salir del juego.

Además, la pantalla muestra un listado de todas las mascotas liberadas previamente,
utilizando la información almacenada por el backend.

Funciones principales:
- pantalla_liberacion(): administra el loop principal de la pantalla, la interacción
  con los botones y la actualización visual.
- dibujar_texto(): función auxiliar para renderizar texto en pantalla.

Dependencias importantes:
- confirmar_liberacion(): registra una nueva liberación en el backend.
- obtener_mascotas_liberadas(): devuelve el historial de mascotas.
- pantalla_huevo(): permite comenzar la creación de una nueva mascota.
- salir_del_juego(): cierra el juego correctamente.
"""
import pygame
import sys
import os
from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego
from frontend.pantallaHuevo import pantalla_huevo
from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego, obtener_mascotas_liberadas

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Liberación")

# Colores
FONDO = (200, 255, 200)
TEXTO = (50, 80, 30)
BOTON = (150, 200, 150)
BOTON_HOVER = (180, 230, 180)
TEXTO_HOVER = (80, 120, 50)

fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)

# Botones
boton_liberar = pygame.Rect(150, 450, 150, 50)
boton_salir = pygame.Rect(500, 450, 150, 50)

def dibujar_texto(texto, fuente, color, x, y):
    """
     Dibuja texto en la ventana del juego.

     Parámetros:
     texto : str
         Cadena que se mostrará en pantalla.
     fuente : pygame.font.Font
         Fuente usada para renderizar el texto.
     color : tuple[int, int, int]
         Color RGB del texto.
     x : int
         Posición horizontal donde se dibujará el texto.
     y : int
         Posición vertical donde se dibujará el texto.
     """
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))
    return superficie 

def pantalla_liberacion():
    """
     Ejecuta la pantalla de liberación de la mascota.

     Esta función controla el loop principal de la pantalla, incluyendo:
     - Renderizado del mensaje principal.
     - Dibujado de botones de interacción.
     - Visualización del historial de mascotas liberadas.
     - Manejo de eventos de clic para liberar la mascota, crear una nueva o salir.

     Flujo de opciones:
     - "Liberar": llama a `confirmar_liberacion()` y vuelve a pantalla_huevo().
     - "Nueva Mascota": reinicia el proceso creando un nuevo huevo.
     - "Salir": ejecuta `salir_del_juego()`.

     El loop continúa hasta que el usuario selecciona alguna acción válida.
     """
    reloj = pygame.time.Clock()

    while True:
        VENTANA.fill(FONDO)

        # --- Título centrado ---
        titulo_texto = "Tu mascota está lista para ser liberada"
        superficie_titulo = fuente_titulo.render(titulo_texto, True, TEXTO)
        ancho_titulo = superficie_titulo.get_width()
        alto_titulo = superficie_titulo.get_height()
        x_titulo = (ANCHO - ancho_titulo) // 2
        y_titulo = 100

        # Hover sobre el título
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(x_titulo, y_titulo, ancho_titulo, alto_titulo).collidepoint(mouse_pos):
            color_titulo = TEXTO_HOVER
        else:
            color_titulo = TEXTO

        dibujar_texto(titulo_texto, fuente_titulo, color_titulo, x_titulo, y_titulo)

        # --- Botones con hover ---
        for boton, texto in [(boton_liberar, "Liberar"), (boton_salir, "Salir")]:
            if boton.collidepoint(mouse_pos):
                color_boton = BOTON_HOVER
            else:
                color_boton = BOTON
            pygame.draw.rect(VENTANA, color_boton, boton)

            # Centrar texto dentro del botón
            superficie_texto = fuente_label.render(texto, True, TEXTO)
            texto_ancho = superficie_texto.get_width()
            texto_alto = superficie_texto.get_height()
            x_texto = boton.x + (boton.width - texto_ancho) // 2
            y_texto = boton.y + (boton.height - texto_alto) // 2
            VENTANA.blit(superficie_texto, (x_texto, y_texto))

        # --- Subtítulo centrado ---
        superficie = fuente_label.render("Mascotas liberadas:", True, TEXTO)
        ancho_texto = superficie.get_width()
        x_centrado = (ANCHO - ancho_texto) // 2
        dibujar_texto("Mascotas liberadas:", fuente_label, TEXTO, x_centrado, 200)

        # Mostrar historial de mascotas liberadas
        mascotas = obtener_mascotas_liberadas()
        y_offset = 250
        for m in mascotas:
            texto = f"- {m['nombre']} ({m['especie']})"
            dibujar_texto(texto, fuente_label, TEXTO, 100, y_offset)
            y_offset += 30

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_liberar.collidepoint(evento.pos):
                    confirmar_liberacion()
                    pantalla_huevo()
                    return
                elif boton_salir.collidepoint(evento.pos):
                    salir_del_juego()
                    return

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_liberacion()











# import pygame
# import sys
# import os
# from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego
# from frontend.pantallaHuevo import pantalla_huevo
# from backend.controlador import confirmar_liberacion, ver_mascotas_liberadas, salir_del_juego, obtener_mascotas_liberadas

# pygame.init()

# ANCHO, ALTO = 800, 600
# VENTANA = pygame.display.set_mode((ANCHO, ALTO))
# pygame.display.set_caption("PawPop - Liberación")

# # Colores
# FONDO = (200, 255, 200)
# TEXTO = (50, 80, 30)
# BOTON = (150, 200, 150)

# fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
# fuente_label = pygame.font.SysFont("Arial", 28)

# # Botones
# boton_liberar = pygame.Rect(150, 450, 150, 50)
# boton_salir = pygame.Rect(500, 450, 150, 50)

# def dibujar_texto(texto, fuente, color, x, y):
#     """
#     Dibuja texto en la ventana del juego.

#     Parámetros:
#     texto : str
#         Cadena que se mostrará en pantalla.
#     fuente : pygame.font.Font
#         Fuente usada para renderizar el texto.
#     color : tuple[int, int, int]
#         Color RGB del texto.
#     x : int
#         Posición horizontal donde se dibujará el texto.
#     y : int
#         Posición vertical donde se dibujará el texto.
#     """
#     superficie = fuente.render(texto, True, color)
#     VENTANA.blit(superficie, (x, y))

# def pantalla_liberacion():
#     """
#     Ejecuta la pantalla de liberación de la mascota.

#     Esta función controla el loop principal de la pantalla, incluyendo:
#     - Renderizado del mensaje principal.
#     - Dibujado de botones de interacción.
#     - Visualización del historial de mascotas liberadas.
#     - Manejo de eventos de clic para liberar la mascota, crear una nueva o salir.

#     Flujo de opciones:
#     - "Liberar": llama a `confirmar_liberacion()` y vuelve a pantalla_huevo().
#     - "Nueva Mascota": reinicia el proceso creando un nuevo huevo.
#     - "Salir": ejecuta `salir_del_juego()`.

#     El loop continúa hasta que el usuario selecciona alguna acción válida.
#     """
#     reloj = pygame.time.Clock()

#     while True:
#         VENTANA.fill(FONDO)
#         superficie_titulo = fuente_titulo.render("Tu mascota está lista para ser liberada", True, TEXTO)
#         ancho_titulo = superficie_titulo.get_width()
#         x_titulo = (ANCHO - ancho_titulo) // 2
#         dibujar_texto("Tu mascota está lista para ser liberada", fuente_titulo, TEXTO, x_titulo, 100)


#         # Botones
#         pygame.draw.rect(VENTANA, BOTON, boton_liberar)
#         pygame.draw.rect(VENTANA, BOTON, boton_salir)

#         dibujar_texto("Liberar", fuente_label, TEXTO, boton_liberar.x + 25, boton_liberar.y + 10)
#         dibujar_texto("Salir", fuente_label, TEXTO, boton_salir.x + 50, boton_salir.y + 10)

        
#         superficie = fuente_label.render("Mascotas liberadas:", True, TEXTO)
#         ancho_texto = superficie.get_width()
#         x_centrado = (ANCHO - ancho_texto) // 2
        
#         # Mostrar historial de mascotas liberadas
#         dibujar_texto("Mascotas liberadas:", fuente_label, TEXTO, x_centrado, 200)

#         mascotas = obtener_mascotas_liberadas()
#         y_offset = 250
#         for m in mascotas:
#             texto = f"- {m['nombre']} ({m['especie']})"
#             dibujar_texto(texto, fuente_label, TEXTO, 100, y_offset)
#             y_offset += 30

#         for evento in pygame.event.get():
#             if evento.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if evento.type == pygame.MOUSEBUTTONDOWN:
#                 if boton_liberar.collidepoint(evento.pos):
#                     confirmar_liberacion()
#                     pantalla_huevo()
#                     return
#                 elif boton_salir.collidepoint(evento.pos):
#                     salir_del_juego()
#                     return

#         pygame.display.flip()
#         reloj.tick(30)

# if __name__ == "__main__":
#     pantalla_liberacion()