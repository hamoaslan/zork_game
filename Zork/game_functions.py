#!/usr/bin/python3
import tkinter as tk
from frotz import Zork
import ed_js
import compass
import load_save

AUTO_UPDATE = True

def auto_update(gui):
    global AUTO_UPDATE
    AUTO_UPDATE = not AUTO_UPDATE
    if AUTO_UPDATE:
        gui.auto_update["text"] = "Update: Enabled"
    else:
        gui.auto_update["text"] = "Update: Disabled"

def update(gui):
    if AUTO_UPDATE:
        # inventory
        gui.inventory['state'] = 'normal'
        gui.inventory.delete(1.0, tk.END)
        gui.inventory.insert(tk.END, "\n".join(gui.zork.command("inventory")))
        gui.inventory['state'] = 'disable'

        # look
        gui.look['state'] = 'normal'
        gui.look.delete(1.0, tk.END)
        gui.look.insert(tk.END, "\n".join(gui.zork.command("look")))
        gui.look['state'] = 'disable'

        # diagnostic
        gui.diagnostic['state'] = 'normal'
        gui.diagnostic.delete(1.0, tk.END)
        gui.diagnostic.insert(tk.END, "\n".join(gui.zork.command("diagnostic")))
        gui.diagnostic['state'] = 'disable'

        # score
        gui.score['state'] = 'normal'
        gui.score.delete(1.0, tk.END)
        gui.score.insert(tk.END, "\n".join(gui.zork.command("score")))
        gui.score['state'] = 'disable'


def submitText(gui, eingabe=""):
    dic_commands = {
        'east': gui.compass.go_east,
        'northeast': gui.compass.go_ne,
        'north': gui.compass.go_north,
        'northwest': gui.compass.go_nw,
        'west': gui.compass.go_west,
        'southwest': gui.compass.go_sw,
        'south': gui.compass.go_south,
        'southeast': gui.compass.go_se,

        'e': gui.compass.go_east,
        'ne': gui.compass.go_ne,
        'n': gui.compass.go_north,
        'nw': gui.compass.go_nw,
        'w': gui.compass.go_west,
        'sw': gui.compass.go_sw,
        's': gui.compass.go_south,
        'se': gui.compass.go_se,
    }

    if eingabe == "":
        eingabe = gui.entry.get()

    eingabe = eingabe.lower()

    if gui.name_toggle == 1:
        if eingabe == 'no':
            gui.textbox['state'] = 'normal'
            gui.textbox.insert(tk.END, '> ' + "Game isn`t saved" + '\n')
            gui.textbox['state'] = 'disable'
            gui.textbox.yview_moveto(1.0)
            gui.entry.delete(0, len(gui.entry.get()))
            return
        gui.command_list.save_entry(eingabe)
        gui.zork.save('./saves/' + eingabe + '.save')
        gui.name_toggle = 0
        gui.entry.delete(0, len(gui.entry.get()))
        gui.textbox['state'] = 'normal'
        gui.textbox.insert(tk.END, '> ' + f"Game saved as {eingabe}.save" + '\n')
        gui.textbox['state'] = 'disable'
        gui.textbox.yview_moveto(1.0)
        return
    # save text
    gui.command_list.cl_append(eingabe)
    # reset idx
    gui.command_list.idx = -1
    if eingabe in dic_commands:
        dic_commands[eingabe](True)

    if 'restore' in eingabe:
        restoref = load_save.askopenfilename()
        # restoref = restoref.split('/')[-1]
        if restoref[-5:] != '.save':
            gui.textbox['state'] = 'normal'
            gui.textbox.insert(tk.END, '> ' + "Please use a game file (.save)" + '\n')
            gui.textbox['state'] = 'disable'
            gui.textbox.yview_moveto(1.0)
            gui.entry.delete(0, len(gui.entry.get()))
            return
        gui.command_list.id = restoref.split('/')[-1][:-5]
        gui.command_list.idx = -1
        gui.command_list.load_list()
        gui.zork.restore(restoref)
        gui.entry.delete(0, len(gui.entry.get()))
        update(gui)
        return

    if 'save' in eingabe:
        gui.textbox['state'] = 'normal'
        gui.textbox.insert(tk.END, '> ' + "Please name your savestate, to skip write 'no'" + '\n')
        gui.textbox['state'] = 'disable'
        gui.textbox.yview_moveto(1.0)
        gui.entry.delete(0, len(gui.entry.get()))
        gui.name_toggle = 1
        return

    # textbox
    gui.textbox['state'] = 'normal'
    gui.textbox.insert(tk.END, '> ' + eingabe + '\n')
    gui.textbox.insert(tk.END, "\n".join(gui.zork.command(eingabe)) + '\n\n')
    gui.textbox['state'] = 'disable'
    gui.textbox.yview_moveto(1.0)

    update(gui)

    gui.entry.delete(0, len(gui.entry.get()))


def command_up(gui):
    gui.entry.delete(0, len(gui.entry.get()))
    gui.command_list.inc_idx()
    gui.entry.insert(tk.END, gui.command_list.get_lastcmd(gui.command_list.idx))


def command_down(gui):
    gui.entry.delete(0, len(gui.entry.get()))
    gui.command_list.dec_idx()
    gui.entry.insert(tk.END, gui.command_list.get_lastcmd(gui.command_list.idx))


def start(gui):
    result = gui.zork.last
    gui.textbox['state'] = 'normal'
    gui.textbox.insert(tk.END, "\n".join(result) + '\n\n')
    gui.textbox['state'] = 'disable'
    gui.textbox.yview_moveto(1.0)

    update(gui)


def drop_item(event, gui):
    line_start = event.widget.index("@%s, %s linestart" % (event.x, event.y))
    line_end = event.widget.index(f"{line_start} lineend")
    line_text = event.widget.get(line_start, line_end)
    submitText(gui, f"drop {line_text.split()[-1]}")


def reset(gui):
    gui.zork.reset()
    gui.textbox['state'] = 'normal'
    gui.textbox.delete(1.0, tk.END)
    gui.textbox.insert(tk.END, "<--------GAME RESET-------->\n")
    gui.clearcmd()
    gui.textbox['state'] = 'disable'
    start(gui)
