from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import copy

class ReproductorVideo(ttk.Frame):

    def __init__(self, parent=None):

        ttk.Frame.__init__(self, parent)

        self.parent = parent

        # privado
        self.__cap = None
        self.__tamaño = (640, 480)
        self.__relacion_imagen = 480 / 640
        self.__reproduciendo = False
        self.__frame = None
        self.__directorio_video = "/"
        self.__video_cargado = False
        self.__total_frames = 0
        self.__tiempo = StringVar()
        self.__tiempo.set("00:00:00")
        self.__velocidad_reproduccion = DoubleVar()
        self.__velocidad_reproduccion.set(1.0)

        # construir widgets
        self.widgets(parent)

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, frame):
        self.__frame = frame
        self.mostrar_frame()

    def widgets(self, parent=None):

        if parent is None:
            self.master.geometry("700x550+0+0")
            self.panel_principal = Frame(self.master, relief=SUNKEN, bg="white")
            self.panel_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        else:
            self.panel_principal = parent

        # panel principal
        self.panel_principal.config(bg="white")

        # frame para mostrar el video
        self.video = Label(self.panel_principal, bg="white")
        self.video.pack(fill=BOTH, expand=True, side=TOP)

        # botones
        self.panel_botones = Frame(self.panel_principal, bg="white")
        self.panel_botones.pack(fill=X, side=BOTTOM)

        self.boton_pausa_reanudar = Button(self.panel_botones, text="Reproducir", command=self.pausar_reanudar_video)
        self.boton_pausa_reanudar.pack(side=LEFT)

        self.boton_detener = Button(self.panel_botones, text="Detener", command=self.detener_video)
        self.boton_detener.pack(side=LEFT)

        # selector de velocidad de reproducción
        self.selector_velocidad = ttk.Combobox(self.panel_botones, textvariable=self.__velocidad_reproduccion, values=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])
        self.selector_velocidad.pack(side=LEFT)

        # contador de tiempo
        self.contador_tiempo = Label(self.panel_botones, textvariable=self.__tiempo)
        self.contador_tiempo.pack(side=RIGHT)

        # barra de progreso
        self.progreso = ttk.Progressbar(self.panel_principal, orient='horizontal', length=200, mode="determinate", style='blue.Horizontal.TProgressbar')
        self.progreso.pack(fill=X, padx=10, pady=10, side=BOTTOM)

        # menú
        menu = Menu(self.panel_principal)
        self.master.config(menu=menu)

        # opciones del menú
        opciones_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=opciones_menu)
        opciones_menu.add_command(label="Abrir archivo", command=self.cargar_video)
        opciones_menu.add_command(label="Salir", command=self.master.destroy)

        # estilo de la barra de progreso
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('blue.Horizontal.TProgressbar', foreground='blue', background='blue')

    def mostrar_frame(self):

        if self.__frame is not None:
            imagen = Image.fromarray(self.__frame)
            imagen.thumbnail(self.__tamaño)
            foto = ImageTk.PhotoImage(image=imagen)
            self.video.config(image=foto)
            self.video.image = foto
            self.video.update()

    def cargar_video(self):

        nombre_video = filedialog.askopenfilename(initialdir=self.__directorio_video,
                                                   title="Seleccionar el video para reproducir",
                                                   filetypes=(("archivos MP4", "*.MP4"),
                                                              ("archivos AVI", "*.AVI"),
                                                              ("todos los archivos", "*.*")))
        if len(nombre_video) != 0:
            self.__directorio_video = os.path.dirname(os.path.abspath(nombre_video))
            self.__cap = cv2.VideoCapture(nombre_video)
            self.__total_frames = int(self.__cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.__video_cargado = True
            self.boton_pausa_reanudar.config(text="Reproducir")
            ret, frame = self.__cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def pausar_reanudar_video(self):
        if self.__video_cargado:
            if self.__reproduciendo:
                self.__reproduciendo = False
                self.boton_pausa_reanudar.config(text="Reproducir")
            else:
                self.__reproduciendo = True
                self.boton_pausa_reanudar.config(text="Pausar")
                self.reproducir_video()

    def detener_video(self):
        if self.__video_cargado:
            self.__reproduciendo = False
            self.boton_pausa_reanudar.config(text="Reproducir")
            self.__cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.__cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.progreso['value'] = 0
            self.__tiempo.set("00:00:00")

    def reproducir_video(self):
        if self.__reproduciendo:
            ret, frame = self.__cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.progreso['value'] = self.__cap.get(cv2.CAP_PROP_POS_FRAMES) / self.__total_frames * 100
                self.__tiempo.set(str(int(self.__cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 // 3600)).zfill(2) + ":" +
                                  str(int(self.__cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 % 3600 // 60)).zfill(2) + ":" +
                                  str(int(self.__cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 % 60)).zfill(2))
            else:
                self.__reproduciendo = False
                self.boton_pausa_reanudar.config(text="Reproducir")
                self.__cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.__cap.read()
                if ret:
                    self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.progreso['value'] = 0
                self.__tiempo.set("00:00:00")
            self.after(int(15 / self.__velocidad_reproduccion.get()), self.reproducir_video)  # Llama a reproducir_video después de 15 milisegundos ajustados por la velocidad de reproducción

if __name__ == "__main__":
    root = Tk()
    ReproductorVideo(root)
    root.mainloop()


