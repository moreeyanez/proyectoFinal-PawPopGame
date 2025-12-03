import pygame
import sys
from backend.controlador import campo, alimentar_mascota, jugar_con_mascota, dormir_mascota

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

def pantalla_casa():
    # Fondos
    fondo_dia = pygame.image.load("assets/Campito (1).png")
    fondo_dia = pygame.transform.scale(fondo_dia, (ANCHO, ALTO))
    fondo_noche = pygame.image.load("assets/campitoNoche.png")
    fondo_noche = pygame.transform.scale(fondo_noche, (ANCHO, ALTO))

    # Diccionario de imágenes por especie y estado
    imagenes_mascotas = {
        "perro": {
            "feliz": "assets/Mascotas/Perrito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Perrito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Perrito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Perrito dormido (2).png",
            "enfermo": "assets/Mascotas/mascotaTriste/Perrito triste.png",
            "empachado": "assets/Mascotas/mascotaEmpachado/Perrito empachadito.png",
            "cansado": "assets/Mascotas/mascotaTriste/Perrito cansado.png"
        },
        "gato": {
            "feliz": "assets/Mascotas/Gatito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Gatito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Gatito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Gatito dormido.png",
            "enfermo": "assets/Mascotas/mascotaTriste/Gatito triste.png",
            "empachado": "assets/Mascotas/mascotaEmpachado/Gatito empachadito.png",
            "cansado": "assets/Mascotas/mascotaTriste/Gatito cansado.png"
        },
        "vaca": {
            "feliz": "assets/Mascotas/Vaquita feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Vaquita jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Vaquita gamer.png",
            "dormido": "assets/Mascotas/mascotaDormido/Vaquita dormida.png",
            "enfermo": "assets/Mascotas/mascotaTriste/Vaquita triste.png",
            "empachado": "assets/Mascotas/mascotaEmpachado/Vaquita empachadita.png",
            "cansado": "assets/Mascotas/mascotaTriste/Vaquita cansada.png"
        },
        "capibara": {
            "feliz": "assets/Mascotas/Carpinchito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Carpinchito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Carpinchito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Carpinchito dormido.png",
            "enfermo": "assets/Mascotas/mascotaTriste/Carpinchito triste.png",
            "empachado": "assets/Mascotas/mascotaEmpachado/Capibara empachadito.png",
            "cansado": "assets/Mascotas/mascotaTriste/Carpinchito cansado.png"
        },
        "conejo": {
            "feliz": "assets/Mascotas/Conejito feliz.png",
            "jugando": "assets/Mascotas/mascotaJugar/Conejito jugar.png",
            "comiendo": "assets/Mascotas/mascotaComerSatis/Conejito satisfecho.png",
            "dormido": "assets/Mascotas/mascotaDormido/Conejito dormido (1).png",
            "enfermo": "assets/Mascotas/mascotaTriste/Conejito triste.png",
            "empachado": "assets/Mascotas/mascotaEmpachado/Conejito empachadito.png",
            "cansado": "assets/Mascotas/mascotaTriste/Conejito cansado.png"
        }
    }

    fondo_actual = fondo_dia
    mascota_x = ANCHO // 2 - 100
    mascota_y = ALTO // 2 - 100

    # Botones principales
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

    # Estado de acción (alimentar/jugar/dormir)
    estado_accion = None
    # Popup de alerta (control)
    mostrar_popup_enfermo = False
    popup_alpha = 160

    while True:
        # Rectángulos del popup (se recalculan cada iteración)
        caja_popup = pygame.Rect(ANCHO // 2 - 220, ALTO // 2 - 120, 440, 220)
        # Único botón del popup: Ir al hospital (centrado)
        boton_hosp = pygame.Rect(caja_popup.x + (caja_popup.width - 160) // 2, caja_popup.y + 130, 160, 44)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Si el popup está activo, solo responde a su botón
                if mostrar_popup_enfermo:
                    if boton_hosp.collidepoint(event.pos):
                        from backend.controlador import enviar_al_hospital
                        enviar_al_hospital()
                        import frontend.pantallaHospital
                        frontend.pantallaHospital.pantalla_hospital()
                        return


                    # Bloquear otras acciones mientras esté el popup
                    continue

                # Acciones principales
                if botones["alimentar"].collidepoint(event.pos):
                    alimentar_mascota()
                    fondo_actual = fondo_dia
                    estado_accion = "comiendo"

                elif botones["jugar"].collidepoint(event.pos):
                    jugar_con_mascota()
                    fondo_actual = fondo_dia
                    estado_accion = "jugando"

                elif botones["dormir"].collidepoint(event.pos):
                    dormir_mascota()
                    fondo_actual = fondo_noche
                    estado_accion = "dormido"

                elif botones["curar"].collidepoint(event.pos):
                    import frontend.pantallaHospital
                    frontend.pantallaHospital.pantalla_hospital()
                    return


        # --- DIBUJAR ---
        VENTANA.blit(fondo_actual, (0, 0))

        # Traer datos con fallback seguro (evita NameError si la mascota no está)
        mascota = getattr(campo, "mascota", None)
        if mascota:
            tipo_mascota = (mascota.ver_especie() or "perro").lower()
            nombre_mascota = mascota.ver_nombre() or "Mascota"
            energia = mascota.ver_energia()
            alimentacion = mascota.ver_alimentacion()
            estado_visual = mascota.obtener_estado_visual() or "feliz"
        else:
            tipo_mascota = "perro"
            nombre_mascota = "Mascota"
            energia = 0
            alimentacion = 0
            estado_visual = "feliz"

        # Prioridad: enfermo > acción > estado visual
        if estado_visual == "enfermo":
            estado_para_mostrar = "enfermo"
            mostrar_popup_enfermo = True
        elif estado_accion:
            estado_para_mostrar = estado_accion
        else:
            estado_para_mostrar = estado_visual

        # Cargar imagen con fallback seguro
        try:
            ruta_img = imagenes_mascotas[tipo_mascota][estado_para_mostrar]
            img_mascota = pygame.image.load(ruta_img)
        except Exception:
            try:
                ruta_img = imagenes_mascotas[tipo_mascota]["feliz"]
                img_mascota = pygame.image.load(ruta_img)
            except Exception:
                # Último fallback: rect simple si faltan imágenes
                img_mascota = pygame.Surface((200, 200))
                img_mascota.fill((200, 100, 100))

        img_mascota = pygame.transform.scale(img_mascota, (200, 200))
        VENTANA.blit(img_mascota, (mascota_x, mascota_y))

        # Nombre y porcentajes
        texto_nombre = fuente.render(nombre_mascota, True, NEGRO)
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, mascota_y + 220))

        texto_energia = fuente.render(f"Energía: {energia}%", True, NEGRO)
        texto_alimento = fuente.render(f"Alimentación: {alimentacion}%", True, NEGRO)
        VENTANA.blit(texto_energia, (50, 30))
        VENTANA.blit(texto_alimento, (50, 70))

        # Botones principales
        for texto, rect in botones.items():
            dibujar_boton(rect, texto.capitalize())

        # Dibujar popup si está activo
        if mostrar_popup_enfermo:
            # Overlay oscuro
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(popup_alpha)
            overlay.fill((0, 0, 0))
            VENTANA.blit(overlay, (0, 0))

            # Caja principal
            pygame.draw.rect(VENTANA, BLANCO, caja_popup, border_radius=12)
            pygame.draw.rect(VENTANA, GRIS, caja_popup, width=2, border_radius=12)

            # Textos
            titulo = fuente.render("¡Tu mascota se enfermó!", True, NEGRO)
            msg = fuente.render("Llévala al hospital para curarla.", True, NEGRO)
            VENTANA.blit(titulo, (caja_popup.x + (caja_popup.width - titulo.get_width()) // 2, caja_popup.y + 30))
            VENTANA.blit(msg, (caja_popup.x + (caja_popup.width - msg.get_width()) // 2, caja_popup.y + 80))

            # Único botón del popup
            pygame.draw.rect(VENTANA, GRIS, boton_hosp, border_radius=8)
            txt_hosp = fuente.render("Ir al hospital", True, NEGRO)
            VENTANA.blit(
                txt_hosp,
                (boton_hosp.x + (boton_hosp.width - txt_hosp.get_width()) // 2, boton_hosp.y + 8)
            )

        pygame.display.flip()

def mostrar_pantalla_casa(mascota):
    """
    Recibe una instancia de mascota y abre la pantalla de Casa.
    La instancia no se usa directamente: la lógica toma campo.mascota.
    Se mantiene la firma para compatibilidad con el flujo existente.
    """
    pantalla_casa()


   