"""
Pantalla del Hospital Veterinario del juego PawPop.

Este módulo muestra el estado de la mascota ingresada al hospital y permite:
- Curarla mediante la función del backend `curar_en_hospital()`.
- Volver a la casa transfiriendo la mascota nuevamente a `campo`.
- Liberarla si está sana, usando `preparar_liberacion()` y luego la pantalla de liberación.

La pantalla incluye:
- Imagen dinámica según especie y estado (feliz/enfermo).
- Estadísticas básicas (energía y alimentación).
- Botones interactivos.
- Popup visual de confirmación de curación.
"""

import pygame
import sys
from backend.controlador import campo, curar_en_hospital, preparar_liberacion
from frontend.pantallaCasa import mostrar_pantalla_casa
from frontend.pantallaLiberacion import pantalla_liberacion
from backend.controlador import hospital, curar_en_hospital, preparar_liberacion, campo 

pygame.init()

# Dimensiones de la ventana principal
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PawPop - Hospital")


FONDO = (240, 255, 240)
TEXTO = (50, 80, 30)
BOTON = (150, 200, 150)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
OVERLAY = (0, 0, 0)

fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_label = pygame.font.SysFont("Arial", 28)

# Botones de la pantalla
boton_curar = pygame.Rect(150, 500, 150, 50)
boton_volver = pygame.Rect(325, 500, 150, 50)
boton_liberar = pygame.Rect(500, 500, 150, 50)

#Fondo del hospital
try:
    fondo_hospital = pygame.image.load("assets/Hospitalito (1).png")
    fondo_hospital = pygame.transform.scale(fondo_hospital, (ANCHO, ALTO))
except Exception:
    fondo_hospital = None

# Diccionario de imágenes de mascotas según especie y estado
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

def dibujar_texto(texto, fuente, color, x, y):
    """
    Renderiza y dibuja un texto en la ventana principal del juego.
    
    - param texto: Texto a renderizar.
    - param fuente: Fuente utilizada para el texto.
    - param color: Color del texto.
    - param x: Coordenada x para dibujar el texto.
    - param y: Coordenada y para dibujar el texto.

    """
    superficie = fuente.render(texto, True, color)
    VENTANA.blit(superficie, (x, y))

def pantalla_hospital():
    """
    Muestra la pantalla principal del hospital veterinario en el juego.

    Esta función gestiona el bucle principal de la pantalla del hospital, incluyendo:
      
      - Renderizado del fondo y elementos gráficos.
      - Visualización de la mascota (enferma o feliz).
      - Botones interactivos: "Curar", "Volver" y "Liberar".
      - Eventos de usuario (clics, cierre de ventana).
      - Integración con backend para curar mascotas y preparar liberación.
      - Popups de confirmación tras acciones exitosas.

    El flujo se mantiene en un bucle infinito hasta que el jugador
    decida volver a la pantalla de casa o liberar la mascota.

    """
    reloj = pygame.time.Clock()
    mostrar_popup_cura = False  
    alpha_overlay = 140

    while True:
       
        if fondo_hospital:
            VENTANA.blit(fondo_hospital, (0, 0))
        else:
            VENTANA.fill(FONDO)

        dibujar_texto("Hospital Veterinario", fuente_titulo, TEXTO, 250, 50)

        # Obtener datos de la mascota ingresada al hospital
        mascota = getattr(hospital, "mascota", None)
        if mascota is None:
            tipo_mascota = "perro"
            nombre_mascota = "Mascota"
            energia = 0
            alimentacion = 0
            estado_visual = "feliz"
        else:
            tipo_mascota = (mascota.ver_especie() or "perro").lower()
            nombre_mascota = mascota.ver_nombre() or "Mascota"
            energia = mascota.ver_energia()
            alimentacion = mascota.ver_alimentacion()
            estado_visual = mascota.obtener_estado_visual() or "feliz"

       
        estado_mostrar = "enfermo" if estado_visual == "enfermo" else "feliz"

       # Cargar y mostrar imagen de la mascota
        try:
            ruta = imagenes_mascotas[tipo_mascota][estado_mostrar]
            img_mascota = pygame.image.load(ruta)
            img_mascota = pygame.transform.scale(img_mascota, (200, 200))
            VENTANA.blit(img_mascota, (ANCHO // 2 - 100, 200))
        except Exception:
            rect = pygame.Surface((200, 200))
            rect.fill((200, 100, 100))
            VENTANA.blit(rect, (ANCHO // 2 - 100, 200))

        # Estadísticas y nombre de la mascota
        texto_nombre = fuente_label.render(nombre_mascota, True, NEGRO)
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, 420))
        texto_energia = fuente_label.render(f"Energía: {energia}%", True, NEGRO)
        texto_alimento = fuente_label.render(f"Alimentación: {alimentacion}%", True, NEGRO)
        VENTANA.blit(texto_energia, (50, 30))
        VENTANA.blit(texto_alimento, (50, 70))

        # Botones
        pygame.draw.rect(VENTANA, BOTON, boton_curar, border_radius=8)
        pygame.draw.rect(VENTANA, BOTON, boton_volver, border_radius=8)
        pygame.draw.rect(VENTANA, BOTON, boton_liberar, border_radius=8)
        dibujar_texto("Curar", fuente_label, TEXTO, boton_curar.x + 40, boton_curar.y + 10)
        dibujar_texto("Volver", fuente_label, TEXTO, boton_volver.x + 40, boton_volver.y + 10)
        if estado_visual != "enfermo":
            pygame.draw.rect(VENTANA, BOTON, boton_liberar, border_radius=8)
            dibujar_texto("Liberar", fuente_label, TEXTO,
                        boton_liberar.x + 30, boton_liberar.y + 10)

  
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if mostrar_popup_cura:
                    caja_popup = pygame.Rect(ANCHO // 2 - 220, ALTO // 2 - 100, 440, 200)
                    boton_aceptar = pygame.Rect(caja_popup.x + (caja_popup.width - 140) // 2,
                                                caja_popup.y + 120, 140, 40)
                    if boton_aceptar.collidepoint(evento.pos):
                        mostrar_popup_cura = False
                    continue
                
                # Curar mascota
                if boton_curar.collidepoint(evento.pos):
                    try:
                        resultado = curar_en_hospital()
                    except Exception as e:
                        print(f"[frontend] Error al curar: {e}")
                        resultado = {"ok": False}

                    if resultado.get("ok"):
                        print(f"[frontend] Curación OK: energía={resultado.get('energia')}, estado={resultado.get('estado')}")
                        mostrar_popup_cura = True
                    else:
                        print(f"[frontend] Curación fallida: {resultado.get('msg')}")
                        mostrar_popup_cura = True


                # Volver a la casa
                elif boton_volver.collidepoint(evento.pos):
                
                    if hospital.mascota:
                        campo.mascota = hospital.mascota
                        hospital.mascota = None
                    mostrar_pantalla_casa(campo.mascota)
                    return

                # Liberar mascota si está sana
                elif boton_liberar.collidepoint(evento.pos):
                    if estado_visual == "enfermo":
                   
                        continue
                    try:
                        preparar_liberacion()
                    except Exception:
                        pass
                    pantalla_liberacion()
                    return

        # Mostrar popup de curación exitosa
        if mostrar_popup_cura:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(alpha_overlay)
            overlay.fill(OVERLAY)
            VENTANA.blit(overlay, (0, 0))

            caja_popup = pygame.Rect(ANCHO // 2 - 220, ALTO // 2 - 100, 440, 200)
            pygame.draw.rect(VENTANA, BLANCO, caja_popup, border_radius=12)
            pygame.draw.rect(VENTANA, TEXTO, caja_popup, width=2, border_radius=12)

            mensaje = fuente_label.render("Mascota curada exitosamente!!", True, NEGRO)
            VENTANA.blit(
                mensaje,
                (caja_popup.x + (caja_popup.width - mensaje.get_width()) // 2,
                 caja_popup.y + 40)
            )

            boton_aceptar = pygame.Rect(caja_popup.x + (caja_popup.width - 140) // 2,
                                        caja_popup.y + 120, 140, 40)
            pygame.draw.rect(VENTANA, BOTON, boton_aceptar, border_radius=8)
            dibujar_texto("Aceptar", fuente_label, TEXTO,
                          boton_aceptar.x + 30, boton_aceptar.y + 8)

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    pantalla_hospital()
