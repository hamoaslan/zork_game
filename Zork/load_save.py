import tkinter as tk
from tkinter.filedialog import askopenfilename


def get_file():
    tk.Tk().withdraw()
    return askopenfilename(initialdir='./saves/')
