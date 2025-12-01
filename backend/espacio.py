from abc import ABC, abstractmethod
from backend.mascota import Mascota
import sys

class Espacio(ABC):
    """
    Clase abstracta para espacios del juego.
    """

    @abstractmethod
    def agregar(self):
        pass

    @abstractmethod
    def alimentar(self):
        pass

    @abstractmethod
    def ver(self):
        pass

    @abstractmethod
    def eliminar(self):
        pass

class Campo(Espacio):
    """
    Espacio donde vive la mascota activa del jugador.
    """

    def __init__(self):
        self.mascota = None

    def agregar(self, nombre, especie):
        """
        Crea una nueva mascota y la agrega al campo.
        """
        self.mascota = Mascota(nombre, especie)
        print("Mascota agregada al campo.")

    def alimentar(self):
        """
        Alimenta a la mascota si existe.
        """
        if self.mascota:
            self.mascota.comer()
        else:
            print("No hay mascota para alimentar.")
    
    def curar_mascota(self, hospital):
        """
        Agrega la mascota al hospital para poder curarla.
        Limpia la referencia en el campo para evitar dobles fuentes de verdad.
        """
        if self.mascota:
            if self.mascota.enfermo:
                hospital.agregar(self.mascota)
                # limpiar referencia en campo
                self.mascota = None
            else:
                print("La mascota no está enferma")
        else:
            print("No hay mascota para curar")

    def ver(self):
        """
        Muestra el estado actual de la mascota.
        """
        if self.mascota:
            self.mascota.ver_estado()
        else:
            print("No hay mascota en el campo.")

    def eliminar(self, libertad):
        """
        Elimina la mascota del campo.
        """
        if self.mascota:
            if self.mascota.enfermo == False:
                libertad.agregar(self.mascota)
                print(f"{self.mascota.ver_nombre()} ha sido eliminada del campo.")
                self.mascota = None 
            else:
                print("La mascota está enferma, antes de liberarla, hay que curarla.")
        else:
            print("No hay mascota para eliminar.")

class Hospital(Espacio):
    """
    Espacio donde se cura la mascota si está enferma.
    """

    def __init__(self):
        self.mascota = None

    def agregar(self, mascota):
        """
        Ingresa la mascota al hospital.
        """
        self.mascota = mascota
        print(f"{mascota.ver_nombre()} ingresó al hospital.")
        
    def alimentar(self):
        """
        En el hospital, alimentar equivale a curar.
        """
        self.curar_mascota()

    def curar_mascota(self):
        """
        Cura a la mascota si está enferma.
        """
        if self.mascota:
            self.mascota.curar()
        else:
            print("No hay mascota en el hospital.")

    def ver(self):
        """
        Muestra el estado de la mascota en el hospital.
        """
        if self.mascota:
            self.mascota.ver_estado()
        else:
            print("No hay mascota en el hospital.")

    def eliminar(self, libertad):
        """
        Libera la mascota del hospital y limpia la referencia.
        """
        if self.mascota:
            if self.mascota.enfermo == False:
                libertad.agregar(self.mascota)
                print(f"{self.mascota.ver_nombre()} fue dada de alta y está lista para ser liberada.")
                # limpiar referencia en hospital
                self.mascota = None
            else:
                print("La mascota está enferma, antes de liberarla, hay que curarla.")
        else:
            print("No hay mascota para liberar.")

class Libertad(Espacio):
    """
    Espacio donde se liberan mascotas sanas.
    """

    def __init__(self):
        self.mascotas_liberadas = []
        self.mascota = None 

    def agregar(self, mascota):
        """
        Agrega a la mascota a la pantalla de liberación si no está enferma.
        """
        if mascota.enfermo == True:
            print(f"{mascota.ver_nombre()} no puede ser liberada porque está enferma.")
        else:
            self.mascota = mascota
            print(f"{mascota.ver_nombre()} está lista para ser liberada.")
    
    def alimentar(self, mascota):
        """
        Las mascotas en libertad no necesitan alimentación. Usamos esta función para liberar oficialmente a la mascota.
        """
        if mascota.enfermo == True:
            print(f"{mascota.ver_nombre()} no puede ser liberada porque está enferma.")
        else:
            self.mascotas_liberadas.append(mascota.get_dict())
            print(f"{mascota.ver_nombre()} ha sido liberada.")

    def ver(self):
        """
        Muestra todas las mascotas liberadas.
        """
        if self.mascotas_liberadas:
            print("Mascotas en libertad:")
            for m in self.mascotas_liberadas:
                print(f"- {m['nombre']} ({m['especie']})")
        else:
            print("No hay mascotas liberadas.")

    def eliminar(self, jugador):
        """
        Borra el historial de mascotas liberadas del jugador.
        Se usa al salir del juego.
        """
        jugador.mascotas_liberadas.clear()
        self.mascota = None 
        print("Historial de mascotas liberadas borrado.")
        sys.exit()

        
