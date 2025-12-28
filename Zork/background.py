#!/usr/bin/python3
import tkinter as tk
from tkinter import Toplevel


class ChatBgApp:
    def __init__(self, gui):
        self.gui = gui
        self.toplevel_open = False

    def mistake(self, select):
        # Nach fehlerhafter Eingabe wird die Eingabebox kurz rot
        if select == 'bg':
            self.eingabeChat['bg'] = "red"
            self.eingabeChat.after(500, lambda: self.eingabeChat.config(bg="lemon chiffon"))
        else:
            self.eingabeWord['bg'] = "red"
            self.eingabeWord.after(500, lambda: self.eingabeWord.config(bg="lemon chiffon"))

    def change(self, select, color):
        # Ändert die Farbe der Textbox
        try:
            if select == 'bg':
                self.gui.textbox.config(bg=color)
            elif select == 'fg':
                self.gui.textbox.config(fg=color)
        except tk.TclError:
            self.mistake(select)

    def chatBg(self):
        if not self.toplevel_open:
            self.gui.background["state"] = tk.DISABLED
            # Erstellen vom neuen Window
            newWindow = Toplevel()
            newWindow.title("Background")
            newWindow.geometry("380x170")
            newWindow.minsize(380, 170)
            newWindow.maxsize(380, 170)

            # Eingabefelder und grid erstellen
            labelChat = tk.Label(newWindow, text="Specify the color of the text box:")
            labelChat.grid(row=0, column=0, sticky="nw")

            self.eingabeChat = tk.Entry(newWindow, bg="lemon chiffon", width=30)
            self.eingabeChat.grid(row=1, column=0, sticky="we")
            self.eingabeChat.bind("<Return>", lambda event: (
            self.change('bg', self.eingabeChat.get()), self.eingabeChat.delete(0, 'end')))

            chatframe = tk.Frame(newWindow)
            chatframe.grid(row=2, column=0, sticky="we")

            labelWord = tk.Label(newWindow, text="Specify the color of the characters:")
            labelWord.grid(row=3, column=0, sticky="nw")

            self.eingabeWord = tk.Entry(newWindow, bg="lemon chiffon", width=30)
            self.eingabeWord.grid(row=4, column=0, sticky="we")
            self.eingabeWord.bind("<Return>", lambda event: (
            self.change('fg', self.eingabeWord.get()), self.eingabeWord.delete(0, 'end')))

            wordframe = tk.Frame(newWindow)
            wordframe.grid(row=5, column=0, sticky="we")

            # Alle nötigen buttons erstellen
            colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White']
            for i, color in enumerate(colors):
                button = tk.Button(chatframe, text=color, command=lambda c=color.lower(): self.change('bg', c))
                button.grid(row=1, column=i, sticky="nw")

            for i, color in enumerate(colors):
                button = tk.Button(wordframe, text=color, command=lambda c=color.lower(): self.change('fg', c))
                button.grid(row=1, column=i, sticky="nw")

            def on_close():
                self.toplevel_open = False
                self.gui.background["state"] = tk.NORMAL
                newWindow.destroy()

            newWindow.protocol("WM_DELETE_WINDOW", on_close)

            newWindow.mainloop()
