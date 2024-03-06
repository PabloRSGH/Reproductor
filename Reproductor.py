import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir archivo", command=self.open_file)

        self.canvas = tk.Canvas(self.master, width=720, height=480)
        self.canvas.pack()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi"), ("Image files", "*.jpg *.png")])
        if self.file_path.endswith((".jpg", ".png")):
            self.image = Image.open(self.file_path)
            self.image = self.image.resize((720, 480), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            # Aquí puedes implementar la lógica para abrir y reproducir el video
            pass

root = tk.Tk()
root.geometry("1280x720")
app = Application(master=root)
app.mainloop()
