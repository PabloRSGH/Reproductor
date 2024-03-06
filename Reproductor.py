import subprocess
import pkg_resources
import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import imageio
from PIL import Image, ImageTk, ImageFilter
import threading

REQUIRED_PACKAGES = [
    'opencv-python',
    'imageio',
    'Pillow'
]

for package in REQUIRED_PACKAGES:
    try:
        dist = pkg_resources.get_distribution(package)
        print('{} ({}) está instalado'.format(dist.key, dist.version))
    except pkg_resources.DistributionNotFound:
        print('{} NO está instalado'.format(package))
        subprocess.call(['pip', 'install', package])

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.playing = False

    def create_widgets(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir archivo", command=self.open_file)

        self.canvas = tk.Canvas(self.master, width=720, height=480)
        self.canvas.pack()

        self.play_button = tk.Button(self.master, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT)

        self.progress = ttk.Scale(self.master, orient="horizontal", length=720)
        self.progress.pack(side=tk.BOTTOM)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi"), ("Image files", "*.jpg *.png")])
        if self.file_path.endswith((".jpg", ".png")):
            self.image = Image.open(self.file_path)
            self.image = self.image.resize((720, 480), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            self.video = imageio.get_reader(self.file_path)
            self.delay = int(1000 / self.video.get_meta_data()['fps'])
            self.play_video()

    def play_video(self):
        self.playing = True
        self.update_frame()

    def update_frame(self):
        if self.playing:
            try:
                frame = self.video.get_next_data()
                frame_image = Image.fromarray(frame)
                frame_image = frame_image.resize((720, 480), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(frame_image)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.after(self.delay, self.update_frame)
            except:
                pass

    def pause_video(self):
        self.playing = False

    def stop_video(self):
        self.playing = False
        self.canvas.delete("all")

root = tk.Tk()
root.geometry("1280x720")
app = Application(master=root)
app.mainloop