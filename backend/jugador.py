import re
from backend.espacio import Campo

class Jugador:
    """
    Representa al jugador del juego PawPop.
    Guarda su nombre, mail y el campo donde vive su mascota.
    """

    def __init__(self, nombre, mail, campo):
        self.__nombre = nombre  # Encapsulado
        self.__mail = mail
        self.campo = campo
        self.mascotas_liberadas = []

        if not self.validar_mail(mail):
            raise ValueError("El mail ingresado no es válido.")

    def validar_mail(self, mail):
        """
        Valida el formato del mail usando expresiones regulares.
        """
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, mail) is not None

    def ver_nombre(self):
        """
        Devuelve el nombre del jugador.
        """
        return self.__nombre

    def ver_mail(self):
        """
        Devuelve el mail del jugador.
        """
        return self.__mail

    def crear_campo(self):
        """
        Accede al campo para interactuar con la mascota.
        """
        print(f"{self.__nombre} entra al campo.")

    def liberar_mascota(self):
        """
        Libera la mascota actual y la guarda en el historial.
        """
        if self.campo.mascota:
            self.mascotas_liberadas.append(self.campo.mascota.get_dict())
            self.campo.eliminar()  # acá se llama al método eliminar del campo
            print("Mascota liberada con éxito.")
        else:
            print("No hay mascota para liberar.")
    
    def ver_mascotas_liberadas(self):
        """
        Devuelve la lista de mascotas liberadas por el jugador.
        """
        return self.mascotas_liberadas
