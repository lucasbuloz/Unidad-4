import json
from classplayer import Jugador

class GestorJugadores:
    def __init__(self, archivo):
        self.__archivo = archivo  # ruta del archivo json
        self.__jugadores = self.cargar_jugadores()

    def cargar_jugadores(self):
        try:
            with open(self.__archivo, 'r') as file:
                data = json.load(file)
                return [Jugador.from_dict(jugador) for jugador in data]
        except FileNotFoundError:
            return []

    def guardar_jugador(self, jugador):
        self.__jugadores.append(jugador)
        self.guardar_jugadores()

    def guardar_jugadores(self):
        with open(self.__archivo, 'w') as file:
            json.dump([jugador.to_dict() for jugador in self.__jugadores], file, indent=4)

    def ver_puntajes(self, tree):
        self.__jugadores.sort(key=lambda x: x.get_puntaje(), reverse=True)
        for jugador in self.__jugadores:
            tree.insert('', 'end', values=(jugador.get_nombre(), jugador.get_fecha(), jugador.get_hora(), jugador.get_puntaje()))
