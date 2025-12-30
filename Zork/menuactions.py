#!/usr/bin/python3
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
from game_functions import submitText
from command_help import ITEMS, HILFE

toplevel_open_help = False
toplevel_open_commands = False

def open_help(gui):
    global toplevel_open_help
    w = 1100
    h = 300

    if not toplevel_open_help:
        toplevel_open_help = True
        map_window = Toplevel(gui)
        map_window.title("Help")
        map_window.geometry(f"{w}x{h}")
        map_window.minsize(w, h)
        map_window.maxsize(w, h)

        textbox = tk.Text(map_window, height=12, width=70)
        textbox.delete(1.0, tk.END)
        textbox.insert(tk.END, HILFE)
        textbox["state"] = tk.DISABLED

        textbox.grid(row=0, column=0, sticky="nswe")
        map_window.grid_rowconfigure(0, weight=1)
        map_window.grid_columnconfigure(0, weight=1)
        
        def on_close():
            global toplevel_open_help
            toplevel_open_help = False
            map_window.destroy()

        map_window.protocol("WM_DELETE_WINDOW", on_close)

        map_window.mainloop()

def open_commands(gui):
    global toplevel_open_commands

    def on_double_click(event):
        index = listbox.curselection()
        if index:
            command = listbox.get(index)
            submitText(gui, command)
        
    def search_items(event):
        search_term = entry.get().lower()
        listbox.delete(0, tk.END)
        for item in ITEMS:
            if search_term in item.lower():
                listbox.insert(tk.END, item)

    w = 300
    h = 400

    if not toplevel_open_commands:
        toplevel_open_commands = True
        commands_window = Toplevel(gui)
        commands_window.title("Command List")
        commands_window.geometry(f"{w}x{h}")
        commands_window.minsize(w, h)
        commands_window.maxsize(w, h)

        entry = tk.Entry(commands_window, bg="lemon chiffon", width=30)
        entry.bind("<KeyRelease>", search_items)
        listbox = tk.Listbox(commands_window, height=20, width=30)
        listbox["selectmode"] = tk.DISABLED
        #listbox.bind("<Double-Button-1>", on_double_click)

        scrollbar = tk.Scrollbar(commands_window)
        scrollbar["command"] = listbox.yview
        listbox["yscrollcommand"] = scrollbar.set

        entry.grid(row=0, column=0, sticky="nswe")
        listbox.grid(row=1, column=0, sticky="nswe")
        scrollbar.grid(row=0, rowspan=2, column=1, sticky="nswe")

        commands_window.grid_columnconfigure(0, weight=1)
        commands_window.grid_rowconfigure(1, weight=1)

        for ele in ITEMS:
            listbox.insert(tk.END, ele)


        def on_close():
            global toplevel_open_commands
            toplevel_open_commands = False
            commands_window.destroy()

        commands_window.protocol("WM_DELETE_WINDOW", on_close)

        commands_window.mainloop()
