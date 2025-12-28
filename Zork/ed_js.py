import tkinter as tk
from tkinter import Toplevel
import json
import os
import datetime


class Command:
    def __init__(self, _id='default'):

        self.id = _id
        self.idx = -1

        # create dir and file if not exist
        if not os.path.exists('./json/save.json'):
            os.system('touch ./json/save.json')
            os.system('cp ./json/layout.json ./json/save.json')

        # Reading from json file
        with open('json/save.json', 'r') as openfile:
            self.commandlist = json.load(openfile)
    
    def save_entry(self, newid):
        # create dir and file if not exist
        if not os.path.exists('./saves/'):
            os.system('mkdir ./saves')
        self.commandlist[newid] = [self.get_date(), self.get_commandlist()]
        self.id = newid
        self.save_commandlist()

    def load_list(self):
        with open('json/save.json', 'r') as openfile:
            self.commandlist = json.load(openfile)

    def get_commandlist(self):
        return self.commandlist[self.id][1]

    def save_commandlist(self):
        # serializing json
        json_object = json.dumps(self.commandlist, indent=4)

        # writing to save.json file
        with open("json/save.json", "w") as outfile:
            outfile.write(json_object)

    def cl_append(self, command):
        # append last commandcd ..
        if command != '' and command is not None:
            if self.commandlist[self.id][1]:
                if self.commandlist[self.id][1][0] != command:
                    self.commandlist[self.id][1].insert(0, command)
            else:
                self.commandlist[self.id][1].insert(0, command)

    def clear_list(self):
        self.commandlist[self.id][1] = []
        self.idx = -1

    def get_lastcmd(self, idx):
        if idx == -1:
            return ''
        else:
            return self.commandlist[self.id][1][idx]

    def get_len(self):
        return len(self.get_commandlist())

    def inc_idx(self):
        if self.idx < self.get_len() - 1:
            self.idx += 1

    def dec_idx(self):
        if self.idx >= 0:
            self.idx -= 1

    def get_date(self):
        date = datetime.datetime.now().strftime('%d%m%Y') + '-' + datetime.datetime.now().strftime('%X')
        return date
       



if __name__ == '__main__':
    c = Command() 
    c.update_date()