import pygame
import sys
import os
from backend.controlador import hospital, campo, curar_en_hospital
from frontend.pantallaCasa import pantalla_casa

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Hospital")

fuente = pygame.font.SysFont("Arial", 32)
boton_curar = pygame.Rect(300, 450, 200, 50)
boton_volver = pygame.Rect(300, 520, 200, 50)

def pantalla_hospital(especie, nombre):
    estado_visual = "enfermo"

    imagenes_mascotas = {
        "perro": {
            "enfermo": "assets/Mascotas/mascotaTriste/Perrito triste.png",
            "feliz": "assets/Mascotas/Perrito feliz.png"
        },
        "gato": {
            "enfermo": "assets/Mascotas/mascotaTriste/Gatito triste.png",
            "feliz": "assets/Mascotas/Gatito feliz.png"
        },
        "vaca": {
            "enfermo": "assets/Mascotas/mascotaTriste/Vaquita triste.png",
            "feliz": "assets/Mascotas/Vaquita feliz.png"
        },
        "capibara": {
            "enfermo": "assets/Mascotas/mascotaTriste/Carpinchito triste.png",
            "feliz": "assets/Mascotas/Carpinchito feliz.png"
        },
        "conejo": {
            "enfermo": "assets/Mascotas/mascotaTriste/Conejito triste.png",
            "feliz": "assets/Mascotas/Conejito feliz.png"
        }
    }

    fondo = pygame.image.load("assets/Hospitalito.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_curar.collidepoint(evento.pos):
                    curar_en_hospital()
                    estado_visual = "feliz"
                elif boton_volver.collidepoint(evento.pos):
                    pantalla_casa(especie, nombre)
                    return

        VENTANA.blit(fondo, (0, 0))

        ruta = imagenes_mascotas[especie.lower()][estado_visual]
        mascota_img = pygame.image.load(ruta)
        mascota_img = pygame.transform.scale(mascota_img, (200, 200))
        VENTANA.blit(mascota_img, (ANCHO // 2 - 100, 180))

        texto_nombre = fuente.render(nombre, True, (0, 0, 0))
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, 400))

        pygame.draw.rect(VENTANA, (200, 255, 200), boton_curar)
        pygame.draw.rect(VENTANA, (200, 200, 255), boton_volver)

        VENTANA.blit(fuente.render("Curar", True, (0, 0, 0)), (boton_curar.x + 60, boton_curar.y + 10))
        VENTANA.blit(fuente.render("Volver", True, (0, 0, 0)), (boton_volver.x + 60, boton_volver.y + 10))

        pygame.display.flip()
        reloj.tick(30)

