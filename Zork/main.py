#!/usr/bin/python3
import tkinter as tk
from PIL import Image, ImageTk
from timer import TimerThread
import compass as comp
from game_functions import submitText, start, command_down, command_up, drop_item, reset, auto_update
import game_functions
from frotz import Zork
from zork_map import open_map_window
import ed_js
from background import ChatBgApp
from menuactions import open_commands, open_help


class GUI(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._root = master
        length = 1020
        height = 580
        self._root.geometry(f"{length}x{height}")
        self._root.minsize(length, height)
        self.zork = Zork(True)

        # Window Name und Icon
        ico = Image.open('images/zork.png')
        icon_photo = ImageTk.PhotoImage(ico)
        self._root.wm_iconphoto(False, icon_photo)
        self._root.title('Zork I')

        self.user = 'default'
        self.command_list = ed_js.Command(self.user)

        self.name_toggle = 0

        self.chatBgApp = ChatBgApp(self)

        self.timer_label = tk.Label(self._root, text="Current session: 00:00:00", bg="lightgrey", anchor="w")
        self.timer = TimerThread(self.update_timer)
        self.timer.start()

        self.menubar = tk.Menu(self._root)
        self._root.config(menu=self.menubar)

        self.btn_frame = tk.Frame(self._root)
        self.textbox = tk.Text(self._root, height=20, width=70, state="disabled", bg="white")

        self.action_frame = tk.Frame(self._root)
        self.eingabe_frame = tk.Frame(self._root)
        self.info_frame = tk.Frame(self._root)
        self.score_frame = tk.Frame(self._root)

        self.create_menubar()
        self.create_btn_frame()
        self.create_action_frame()
        self.create_entry_frame()
        self.create_info_frame()
        self.create_score_frame()
        self.gui_config()
        start(self)

    def create_menubar(self):
        menu_datei = tk.Menu(self.menubar, tearoff=False)
        menu_datei.add_command(label="Load", command=lambda: self.load_f())
        menu_datei.add_command(label="Save", command=lambda: self.save_2f())
        self.menubar.add_cascade(label="Save/Load", menu=menu_datei)

        menu_kommandos = tk.Menu(self.menubar, tearoff=False)
        menu_kommandos.add_command(label="list all", command=lambda: open_commands(self))
        self.menubar.add_cascade(label="Commands", menu=menu_kommandos)

        menu_hilfe = tk.Menu(self.menubar, tearoff=False)
        menu_hilfe.add_command(label="Hints", command=lambda: open_help(self))
        self.menubar.add_cascade(label="Help", menu=menu_hilfe)

    def create_btn_frame(self):
        self.reset = tk.Button(self.btn_frame, text="Reset", command=lambda: reset(self))
        self.quit = tk.Button(self.btn_frame, text="Quit", command=self.closing, )
        self.map = tk.Button(self.btn_frame, text="Map", command=lambda: open_map_window(self))
        self.background = tk.Button(self.btn_frame, text="Background", command=lambda: self.chatBgApp.chatBg())

        # grid
        self.reset.grid(row=0, column=0, sticky="w")
        self.quit.grid(row=0, column=1, sticky="w")
        self.map.grid(row=0, column=2, sticky="w")
        self.background.grid(row=0, column=3, sticky="w")

    def create_action_frame(self):
        self.up = tk.Button(self.action_frame, text="up", command=lambda: submitText(self, "up"))
        self.down = tk.Button(self.action_frame, text="down", command=lambda: submitText(self, "down"))

        self.auto_update = tk.Button(self.action_frame, text="Update: Enabled", command= lambda:auto_update(self))

        self.read_leaflet = tk.Button(self.action_frame, text="read leaflet",command=lambda: submitText(self, "read leaflet"))
        self.take_all = tk.Button(self.action_frame, text="take all", command=lambda: submitText(self, "take all"))
        self.drop_all = tk.Button(self.action_frame, text="drop all", command=lambda: submitText(self, "drop all"))
        self.diagnostic = tk.Button(self.action_frame, text="diagnostic",command=lambda: submitText(self, "diagnostic"))
        self.inv = tk.Button(self.action_frame, text="inventory", command=lambda: submitText(self, "inventory"))

        self.frame_compass = tk.Frame(self.action_frame)
        self.compass = comp.Compass(self.frame_compass, self, 125)

        self.frame_compass.grid(row=0, rowspan=2, column=0, sticky='we')

        self.up.grid(row=0, column=1, sticky="nswe")
        self.down.grid(row=1, column=1, sticky="nswe")
        self.auto_update.grid(row=1, column=2, sticky="nswe")
        self.read_leaflet.grid(row=0, column=2, sticky="nswe")
        self.take_all.grid(row=0, column=3, sticky="nswe")
        self.drop_all.grid(row=1, column=3, sticky="nswe")
        self.diagnostic.grid(row=0, column=4, sticky="nswe")
        self.inv.grid(row=1, column=4, sticky="nswe")

    def compass_interact(self, string):
        submitText(self, string)

    def create_entry_frame(self):
        self.entry = tk.Entry(self.eingabe_frame, bg="lemon chiffon", width=57)
        self.entry.bind("<Return>", lambda event: submitText(self))
        self.entry.bind("<Down>", lambda event: command_down(self))
        self.entry.bind("<Up>", lambda event: command_up(self))
        self.submit = tk.Button(self.eingabe_frame, text="Submit", command=lambda: submitText(self))

        # grid
        self.entry.grid(row=0, column=0, sticky="wens")
        self.submit.grid(row=0, column=1, sticky="ew")

    def create_info_frame(self):
        zork_img = Image.open("images/zork.png")
        zork_img = zork_img.resize((300, 100))
        photo = ImageTk.PhotoImage(zork_img)
        label_img = tk.Label(self.info_frame, image=photo, bg="black")
        label_img.photo = photo

        label_inventory = tk.Label(self.info_frame, text="Inventory")
        self.inventory = tk.Text(self.info_frame, height=5, width=30, state="disabled", bg="dark khaki")
        self.inventory.bind("<Double-1>", lambda event: drop_item(event, self))

        label_look = tk.Label(self.info_frame, text="Look")
        self.look = tk.Text(self.info_frame, height=5, width=30, bg="dark khaki")

        # grid
        label_img.grid(row=0, column=0, columnspan=2, sticky="we")
        label_inventory.grid(row=1, column=0, columnspan=2, sticky="we")
        self.inventory.grid(row=2, column=0, columnspan=2, sticky="nswe")
        label_look.grid(row=3, column=0, columnspan=2, sticky="we")
        self.look.grid(row=4, column=0, columnspan=2, sticky="nswe")

    def create_score_frame(self):
        self.label_diagnostic = tk.Label(self.score_frame, text="Diagnostic")
        self.diagnostic = tk.Text(self.score_frame, height=3, width=30, state="disabled", bg="dark khaki")
        self.label_score = tk.Label(self.score_frame, text="Score")
        self.score = tk.Text(self.score_frame, height=3, width=30, state="disabled", bg="dark khaki")

        # grid
        self.label_diagnostic.grid(row=0, column=0, sticky="we")
        self.diagnostic.grid(row=1, column=0, sticky="we")
        self.label_score.grid(row=2, column=0, sticky="we")
        self.score.grid(row=3, column=0, sticky="we")

    def gui_config(self):
        self.btn_frame.grid(row=0, column=0, sticky="w")
        self.textbox.grid(row=1, column=0, sticky="nswe")
        self.action_frame.grid(row=2, column=0, sticky="w")

        self.eingabe_frame.grid(row=3, column=0, sticky="wse")
        self.eingabe_frame.grid_columnconfigure(0, weight=1)

        self.info_frame.grid(row=1, column=1, sticky="ensw")
        self.info_frame.grid_rowconfigure(2, weight=1)
        self.info_frame.grid_rowconfigure(4, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.score_frame.grid(row=2, rowspan=2, column=1, sticky="swe")
        self.score_frame.grid_columnconfigure(0, weight=1)
        self.timer_label.grid(row=4, column=0, columnspan=2, sticky="se")

        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=3)
        self._root.grid_columnconfigure(1, weight=1)
        self._root.protocol("WM_DELETE_WINDOW", self.closing)

    def update_timer(self, timer_text):
        self.timer_label.config(text=timer_text)

    def closing(self):
        self.command_list.save_commandlist()
        self.timer.stop()
        self._root.destroy()

    def clearcmd(self):
        self.command_list.clear_list()  # clears cmd list due resetting

    # 2 functions for save and load gamefiles
    def load_f(self):
        game_functions.submitText(self, 'restore')

    def save_2f(self):
        game_functions.submitText(self, 'save')


def main():
    gui = GUI(tk.Tk())
    gui._root.mainloop()


if __name__ == '__main__':
    main()
