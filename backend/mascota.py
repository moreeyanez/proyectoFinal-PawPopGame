class Mascota:
    """
    Representa una mascota virtual con estados de energía y alimentación.
    """
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie
        self.comida = self.definir_comida_por_especie(especie)
        self.__energia = 80  # Encapsulado
        self.__alimentacion = 80  # Encapsulado
        self.enfermo = False

    def ver_nombre(self):
        """
        Devuelve el nombre de la mascota.
        Útil para mostrarla en la interfaz gráfica.
        """
        return self.nombre
    
    def ver_comida(self):
        """
        Devuelve la comida favorita de la mascota.
        Útil para mostrarla en la interfaz gráfica.
        """
        return self.comida

    def ver_especie(self):
        """
        Devuelve la especie de la mascota.
        Permite al front acceder a esta información sin modificarla.
        """
        return self.especie
    
    def definir_comida_por_especie(self, especie):
        """
        Devuelve la comida favorita asociada a una especie.
        """
        comidas = {
            "Perro": "Croquetas",
            "Gato": "Atún",
            "Vaca": "Pasto",
            "Conejo": "Zanahorias",
            "Capibara": "Frutas"
        }
        return comidas.get(especie, "Comida genérica")

    def dormir(self):
        """
        La mascota duerme y recupera energía.
        """
        self.modificar_energia(+20)
        print(f"{self.nombre} está durmiendo... Energía: {self.ver_energia()}")

    def comer(self):
        """
        La mascota come. Si se sobrealimenta, se enferma.
        """
        self.modificar_alimentacion(+20)
        print(f"{self.nombre} está comiendo {self.comida}. Alimentación: {self.ver_alimentacion()}")
        if self.enfermo:
            print(f"{self.nombre} se empachó y está enferma.")

    def jugar(self):
        """
        La mascota juega. Esto baja la energía y la alimentación.
        Si la energía baja demasiado, se enferma.
        """
        self.modificar_energia(-30)
        self.modificar_alimentacion(-10)
        print(f"{self.nombre} está jugando. Energía: {self.ver_energia()}, Alimentación: {self.ver_alimentacion()}")
        if self.enfermo:
            print(f"{self.nombre} se cansó demasiado y está enferma.")

    def curar(self):
        """
        Cura a la mascota si está enferma. Restaura energía y alimentación.
        """
        if self.enfermo:
            self.enfermo = False
            self.__energia = 80
            self.__alimentacion = 80
            print(f"{self.nombre} ha sido curada.")
        else:
            print(f"{self.nombre} no está enferma.")

    def modificar_energia(self, cantidad):
        """
        Modifica el nivel de energía de la mascota.
        Asegura que el valor se mantenga entre 0 y 100.
        Si la energía baja de 50, la mascota se enferma.
        """
        self.__energia = max(0, min(self.__energia + cantidad, 100))
        if self.__energia < 50:
            self.enfermo = True

    def modificar_alimentacion(self, cantidad):
        """
        Modifica el nivel de alimentación de la mascota.
        Asegura que el valor se mantenga entre 0 y 120.
        Si la alimentación supera 100, la mascota se enferma.
        """
        self.__alimentacion = max(0, min(self.__alimentacion + cantidad, 120))
        if self.__alimentacion > 100:
            self.enfermo = True

    def ver_energia(self):
        """
        Devuelve el nivel de energía.
        """
        return self.__energia

    def ver_alimentacion(self):
        """
        Devuelve el nivel de alimentación.
        """
        return self.__alimentacion
    
    def ver_estado(self):
        """
        Muestra el estado actual de la mascota.
        """
        print(f"Nombre: {self.nombre}")
        print(f"Especie: {self.especie}")
        print(f"Comida favorita: {self.comida}")
        print(f"Energía: {self.ver_energia()}")
        print(f"Alimentación: {self.ver_alimentacion()}")
        print(f"¿Enferma?: {self.enfermo}")
    
    def get_dict(self):
        """
        Devuelve un diccionario con los datos actuales de la mascota.
        Útil para guardar el estado en un archivo JSON.
        """
        return {
            "nombre": self.nombre,
            "especie": self.especie,
            "comida": self.comida,
            "energia": self.ver_energia(),
            "alimentacion": self.ver_alimentacion(),
            "enfermo": self.enfermo,
            "estado": "liberada"
        }

    def obtener_estado_visual(self):
        """
        Devuelve el estado visual de la mascota para mostrar la imagen correspondiente.
        """
        if self.enfermo:
            return "enfermo"
        elif self.ver_energia() < 50:
            return "cansado"
        elif self.ver_alimentacion() > 100:
            return "empachado"
        else:
            return "feliz"
        


