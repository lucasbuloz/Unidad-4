import tkinter as tk
import random
from tkinter import messagebox, Menu, ttk
from gestor import GestorJugadores
from classplayer import Jugador
import datetime

class SimonDice:
    def __init__(self, ventana):
        self.__ventana = ventana
        self.__ventana.title("Py-SimonGame")
        self.__ventana.geometry("300x350")  

        self.__color = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
        self.__secuencia = []
        self.__secuencia_user = []
        self.__secuencia_user_active = False
        self.__gestor_jugadores = GestorJugadores("pysimonpuntajes.json")
        
        self.__nombre_usuario = ""
        self.__puntaje = 0

        self.__label_info = tk.Label(self.__ventana, text="Nombre: -- | Puntaje: 0", font=("Arial", 12))
        self.__label_info.pack(pady=10)

        self.__frame_botones = tk.Frame(self.__ventana)
        self.__frame_botones.pack(expand=True, fill="both")
        
        self.__botonverde = self.create_button(self.__color[0])
        self.__botonrojo = self.create_button(self.__color[1])
        self.__botonazul = self.create_button(self.__color[2])
        self.__botonamarillo = self.create_button(self.__color[3])
        
        self.__botonverde.grid(row=0, column=0, sticky="nsew")
        self.__botonrojo.grid(row=0, column=1, sticky="nsew")
        self.__botonazul.grid(row=1, column=0, sticky="nsew")
        self.__botonamarillo.grid(row=1, column=1, sticky="nsew")
        
        self.__frame_botones.grid_rowconfigure(0, weight=1)
        self.__frame_botones.grid_rowconfigure(1, weight=1)
        self.__frame_botones.grid_columnconfigure(0, weight=1)
        self.__frame_botones.grid_columnconfigure(1, weight=1)
        
        self.mostrar_dialogo_usuario()
        self.crear_menu()

    def create_button(self, color):
        canvas = tk.Canvas(self.__frame_botones, bg=color, width=100, height=100, relief="raised")
        canvas.bind("<Button-1>", lambda event, c=color: self.on_button_click(event, canvas, c))
        return canvas

    def iniciar_juego(self):
        self.__secuencia = []
        self.__secuencia_user = []
        self.__secuencia_user_active = False
        self.__puntaje = 0
        self.actualizar_info()
        self.agregar_color_juego()

    def agregar_color_juego(self):
        self.__secuencia.append(random.choice(self.__color))
        self.mostrar_secuencia()

    def mostrar_secuencia(self):
        delay = 1000  
        for i, color in enumerate(self.__secuencia):
            self.__ventana.after(delay * i, lambda color=color: self.cambiar_color_botones(color))
            self.__ventana.after(delay * i + delay // 2, self.restaurar_color_botones)
        self.__ventana.after(delay * len(self.__secuencia), self.activar_botones)

    def cambiar_color_botones(self, color):
        if color == self.__color[0]:
            self.__botonverde.config(bg="#ffffff")
        elif color == self.__color[1]:
            self.__botonrojo.config(bg="#ffffff")
        elif color == self.__color[2]:
            self.__botonazul.config(bg="#ffffff")
        elif color == self.__color[3]:
            self.__botonamarillo.config(bg="#ffffff")

    def restaurar_color_botones(self):
        self.__botonverde.config(bg=self.__color[0])
        self.__botonrojo.config(bg=self.__color[1])
        self.__botonazul.config(bg=self.__color[2])
        self.__botonamarillo.config(bg=self.__color[3])

    def on_button_click(self, event, canvas, color):
        if not self.__secuencia_user_active:
            return
        canvas.config(bg="#ffffff")
        self.__ventana.after(500, lambda: canvas.config(bg=color))
        self.__secuencia_user.append(color)
        if self.__secuencia[:len(self.__secuencia_user)] == self.__secuencia_user:
            if len(self.__secuencia) == len(self.__secuencia_user):
                self.__puntaje += 1
                self.actualizar_info()
                self.__secuencia_user = []
                self.__secuencia_user_active = []
                self.desactivar_botones()
                self.__ventana.after(1000, self.agregar_color_juego)
        else:
            messagebox.showinfo("GAME OVER", f"GAME OVER. Tu puntuación final es: {self.__puntaje}")
            self.guardar_puntaje_final()
            self.reset_juego()

    def guardar_puntaje_final(self):
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        nuevo_jugador = Jugador(self.__nombre_usuario, fecha_actual, hora_actual, self.__puntaje)
        self.__gestor_jugadores.guardar_jugador(nuevo_jugador)

    def desactivar_botones(self):
        self.__botonverde.unbind("<Button-1>")
        self.__botonrojo.unbind("<Button-1>")
        self.__botonazul.unbind("<Button-1>")
        self.__botonamarillo.unbind("<Button-1>")
        self.__secuencia_user_active = False

    def activar_botones(self):
        self.__botonverde.bind("<Button-1>", lambda event: self.on_button_click(event, self.__botonverde, self.__color[0]))
        self.__botonrojo.bind("<Button-1>", lambda event: self.on_button_click(event, self.__botonrojo, self.__color[1]))
        self.__botonazul.bind("<Button-1>", lambda event: self.on_button_click(event, self.__botonazul, self.__color[2]))
        self.__botonamarillo.bind("<Button-1>", lambda event: self.on_button_click(event, self.__botonamarillo, self.__color[3]))
        self.__secuencia_user_active = True

    def mostrar_dialogo_usuario(self):
        self.__dialogo = tk.Toplevel(self.__ventana)
        self.__dialogo.geometry('300x200')
        self.__dialogo.resizable(0, 0)
        tk.Label(self.__dialogo, text="Nombre de Usuario:").pack()
        self.__nombre_entrada = tk.Entry(self.__dialogo)
        self.__nombre_entrada.pack()
        self.__boton_confirmar = tk.Button(self.__dialogo, text='Confirmar', command=self.guardar_nombre_usuario)
        self.__boton_confirmar.pack()

    def guardar_nombre_usuario(self):
        self.__nombre_usuario = self.__nombre_entrada.get()
        self.__dialogo.destroy()
        self.iniciar_juego()

    def reset_juego(self):
        self.__secuencia = []
        self.__secuencia_user = []
        self.__secuencia_user_active = False
        self.__puntaje = 0
        self.iniciar_juego()

    def actualizar_info(self):
        self.__label_info.config(text=f"Nombre: {self.__nombre_usuario} | Puntaje: {self.__puntaje}")

    def crear_menu(self):
        menubar = Menu(self.__ventana)
        self.__ventana.config(menu=menubar)
        opciones_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="☰", menu=opciones_menu) 
        opciones_menu.add_command(label="Ver puntajes", command=self.ver_puntajes)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.__ventana.quit)

    def ver_puntajes(self):
        puntajes_ventana = tk.Toplevel(self.__ventana)
        puntajes_ventana.title("Puntajes")
        puntajes_ventana.geometry("400x300")

        tree = ttk.Treeview(puntajes_ventana, columns=('Jugador', 'Fecha', 'Hora', 'Puntaje'), show='headings')
        tree.heading('Jugador', text='Jugador')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Hora', text='Hora')
        tree.heading('Puntaje', text='Puntaje')
        
        tree.column('Jugador', width=50)
        tree.column('Fecha', width=50)
        tree.column('Hora', width=50)
        tree.column('Puntaje', width=20)

        tree.pack(expand=True, fill='both')

        self.__gestor_jugadores.ver_puntajes(tree)

        close_button = tk.Button(puntajes_ventana, text='Cerrar', command=puntajes_ventana.destroy)
        close_button.pack(pady=10)

if __name__ == '__main__':
    ventana = tk.Tk()
    juego = SimonDice(ventana)
    ventana.mainloop()
