from tkinter import *
import webbrowser
import subprocess
import itertools
import re
import os
import configparser
from urllib.parse import urlparse

def is_url(path):
    return 'http' in urlparse(path).scheme

def is_file(path):
    return os.path.isfile(path)

bg_color='#505050'
fg_color='#00f2b2'
insert_color='#ffffff'
list_font = ('Helvetica', 18)
FILENAME = 'quick_access.cfg'

config = configparser.RawConfigParser()
keywordmap = dict()


def generate_sections(config):
    sections = ['items','unnamed']
    for section in sections:
        if not config.has_section(section):
            config.add_section(section)
            with open(FILENAME,'w') as configfile:
                config.write(configfile)

def starter(path,args=[]):
    if   is_url(path):
        return lambda args=args: webbrowser.open_new_tab(path+' '.join(args))
    elif is_file(path):
        try:
            return lambda args=args: subprocess.Popen([path]+args)
        except IOError:
            executable = os.path.basename(path)
            return lambda args=args: subprocess.Popen([executable]+args,cwd=os.path.dirname(path))
    return lambda args=args: None

class AccessItem:
    def __init__(self,section,keyword,value,function):
        self.section = section
        self.keyword = keyword
        self.value = value
        self.function = function

def setup():
    config.read(FILENAME)
    generate_sections(config)

    for section in config.sections():
        items = sorted(config.items(section),key=lambda item: item[0])
        for option,value in items:
            option = option.lower()
            if section == 'items':
                keywordmap[option] = AccessItem(section,option,value,starter(value))

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.lista = sorted(lista)
        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.words = self.comparison()
        self.lb = None
        self.after(150,lambda: self.changed(None,None,None))

    def create_listbox(self):
        self.lb = Listbox(bg=bg_color,fg=fg_color,height=len(self.words),font=list_font)
        self.lb.bind("<Right>", self.selection)
        self.lb.bind("<FocusIn>", self.selection)
        self.lb.bind("<MouseWheel>", lambda event: self.move_selection(event.delta//120))
        self.lb.bind("<Motion>", lambda event: self.set_selection(self.lb.nearest(event.y)))
        self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
        
    def changed(self, name, index, mode):
        self.words = self.comparison()
        if self.words:
            if self.lb:
                self.lb.destroy()
                self.lb = None
            if self.lb is None or len(self.words) != self.lb.size():
                self.create_listbox()
            
            self.lb.delete(0, END)
            for w in self.words:
                self.lb.insert(END,w)
            self.lb.selection_set(first='0')
            self.lb.activate('0')
        
    def selection(self, event):
        if self.lb:
            front_parts = self.var.get().split(',')[:-1]
            text = ','.join(front_parts + [self.lb.get(ACTIVE)])
            self.var.set(text)
            if self.lb:
                self.lb.destroy()
                self.lb = None
            self.icursor(END)
            self.focus_set()

    def set_selection(self, index):
        if self.lb:
            index = str(((int(index))%self.lb.size()))
            self.lb.selection_clear(first=0,last=END)
            self.lb.selection_set(first=index)
            self.lb.activate(index)

    def move_selection(self,amount):
        if self.lb:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                if not self.words:
                    self.words = self.comparison()
                index = str(((int(index)-amount)%self.lb.size()))
                self.lb.selection_set(first=index)
                self.lb.activate(index)
            
    def up(self, event):
        self.move_selection(1)

    def down(self, event):
        self.move_selection(-1)

    def comparison(self):
        last_part = self.var.get().split(',')[-1].strip()
        if last_part:
            ret_list = [w for w in self.lista if re.search(last_part, w)]
            return ret_list
        return self.lista

class Application:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        ws,hs = self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.entry = AutocompleteEntry(master=self.root,lista=keywordmap.keys(),
            bg=bg_color,fg=fg_color,insertbackground=insert_color,
            insertwidth=6,
            width=ws,font=("Helvetica", -60),
            borderwidth=1, relief=SUNKEN
            )
        self.entry.pack(padx=80,pady=80)
        self.entry.focus_set()
        
        self.root.geometry('%dx%d+%d+%d' % (ws, hs, 0, 0))
        
        self.root.configure(background='pink')
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparent", "pink")
        
        self.root.bind('<Escape>',self.quit)
        # self.root.bind('<Motion>',self.quit)
        # self.root.bind('<Button-1>',self.quit)
        # self.root.bind('<Button-2>',self.quit)
        # self.root.bind('<Button-3>',self.quit)
        self.root.bind('<Return>',self.text_entry)
        self.root.bind('<Control-Key-s>',self.save_entry)
    
    def get_parts(self):
        text = self.entry.get().lower()
        parts = text.strip().split(',')
        parts = [part.strip() for part in parts if part]
        return parts

    def text_entry(self,event):
        parts = self.get_parts()
        for part in parts:
            subparts = part.split()
            kw = subparts[0:1][0]
            args = subparts[1:]
            if kw in keywordmap:
                keywordmap[kw].function(args)
        self.quit()

    def save_entry(self,event):
        parts = self.get_parts()
        counter = 0
        RENAMEME = 'rename_me_'
        if not config.has_section('unnamed'):
            config.add_section('unnamed')
        else:
            options = config.options('unnamed')
            for option in options:
                number_str = option.split(RENAMEME)[-1:][0]
                if number_str.isdigit():
                    number = int(number_str)
                    counter = max(counter,number)+1
        for part in parts:
            subparts = part.split()
            kw = subparts[0:1][0]
            args = subparts[1:]
            value = None
            if kw in keywordmap:
                value = keywordmap[kw].value
                if value is not None:
                    config.set('unnamed',RENAMEME+str(counter),value+' '.join(args))
                    with open(FILENAME, 'w') as configfile:
                        config.write(configfile)
    
    def quit(self,event=None):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
    
if __name__ == '__main__':
    setup()
    Application().run()