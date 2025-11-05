import os
import pygame
import sys

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Casa")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (220, 220, 220)

fuente = pygame.font.Font(None, 36)

# --- FUNCIÓN PRINCIPAL ---
def pantalla_casa(tipo_mascota, nombre_mascota):
    # Imágenes de fondo
    fondo_dia = pygame.image.load("assets/Campito (1).png")
    fondo_dia = pygame.transform.scale(fondo_dia, (ANCHO, ALTO))
    fondo_noche = pygame.image.load("assets/campitoNoche.png")
    fondo_noche = pygame.transform.scale(fondo_noche, (ANCHO, ALTO))

    imagenes_mascotas = {
        "perro": {
            "normal": "assets/Mascotas/Perrito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Perrito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Perrito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Perrito dormido (2).png"
        },
        "gato": {
            "normal": "assets/Mascotas/Gatito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Gatito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Gatito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Gatito dormido.png"
        },
        "vaca": {
            "normal": "assets/Mascotas/Vaquita feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Vaquita jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Vaquita gamer.png",
            "dormido": "assets/Mascotas/mascotaDormido/Vaquita dormida.png"
        },
        "capibara": {
            "normal": "assets/Mascotas/Carpinchito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Carpinchito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Carpinchito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Carpinchito dormido.png"
        },
        "conejo": {
            "normal": "assets/Mascotas/Conejito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Conejito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Conejito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Conejito dormido (1).png"
        }
    }

    # Estado inicial
    estado = "normal"
    fondo_actual = fondo_dia

    # Porcentajes iniciales (para futuro uso)
    energia = 100
    alimentacion = 100

    # Posición de mascota
    mascota_x = ANCHO // 2 - 100
    mascota_y = ALTO // 2 - 100

    # --- BOTONES ---
    botones = {
        "alimentar": pygame.Rect(100, 500, 120, 50),
        "jugar": pygame.Rect(250, 500, 120, 50),
        "dormir": pygame.Rect(400, 500, 120, 50),
        "curar": pygame.Rect(550, 500, 120, 50)
    }

    def dibujar_boton(rect, texto):
        pygame.draw.rect(VENTANA, GRIS, rect, border_radius=8)
        texto_render = fuente.render(texto, True, NEGRO)
        VENTANA.blit(
            texto_render,
            (rect.x + (rect.width - texto_render.get_width()) // 2,
             rect.y + (rect.height - texto_render.get_height()) // 2)
        )

    # --- LOOP PRINCIPAL ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botones["alimentar"].collidepoint(event.pos):
                    estado = "comiendo"
                    fondo_actual = fondo_dia
                elif botones["jugar"].collidepoint(event.pos):
                    estado = "jugando"
                    fondo_actual = fondo_dia
                elif botones["dormir"].collidepoint(event.pos):
                    estado = "dormido"
                    fondo_actual = fondo_noche
                elif botones["curar"].collidepoint(event.pos):
                    # Ir a pantalla hospital
                    import pantallaHospital
                    pantallaHospital.pantalla_hospital(tipo_mascota, nombre_mascota)

        # --- DIBUJAR ---
        VENTANA.blit(fondo_actual, (0, 0))

        # Imagen de la mascota según estado
        img_mascota = pygame.image.load(imagenes_mascotas[tipo_mascota][estado])
        img_mascota = pygame.transform.scale(img_mascota, (200, 200))
        VENTANA.blit(img_mascota, (mascota_x, mascota_y))

        # Nombre y porcentajes
        texto_nombre = fuente.render(nombre_mascota, True, NEGRO)
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, mascota_y + 220))

        texto_energia = fuente.render(f"Energía: {energia}%", True, NEGRO)
        texto_alimento = fuente.render(f"Alimentación: {alimentacion}%", True, NEGRO)
        VENTANA.blit(texto_energia, (50, 30))
        VENTANA.blit(texto_alimento, (50, 70))

        # Botones
        for texto, rect in botones.items():
            dibujar_boton(rect, texto.capitalize())

        pygame.display.flip()


def mostrar_pantalla_casa(mascota):
    """
    Recibe una instancia
    """
    especie = mascota.ver_especie()
    nombre = mascota.ver_nombre()

    pantalla_casa(especie.lower(), nombre)

   