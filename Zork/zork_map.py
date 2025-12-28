#!/usr/bin/python3
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk

toplevel_open = False


def open_map_window(gui):
    global toplevel_open
    w = 1200
    h = 700

    if not toplevel_open:
        toplevel_open = True
        map_window = Toplevel(gui)
        map_window.title("Map")
        map_window.geometry(f"{w}x{h}")
        map_window.minsize(w, h)
        map_window.maxsize(w, h)

        img = Image.open("images/zork1_map.png")
        img = img.resize((w, h))

        map_image = ImageTk.PhotoImage(img)
        map_label = tk.Label(map_window, image=map_image)
        map_label.pack(fill=tk.BOTH, expand="yes")

        def on_close():
            global toplevel_open
            toplevel_open = False
            map_window.destroy()

        map_window.protocol("WM_DELETE_WINDOW", on_close)

        map_window.mainloop()
